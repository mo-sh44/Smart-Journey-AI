from datetime import datetime

from services.flight_service import FlightService
from services.hotel_service import HotelService
from services.memory_service import MemoryService
from services.travel_agency_service import TravelAgencyService
from services.weather_service import WeatherService


class MonitoringService:
    def __init__(self):
        self.memory = MemoryService()
        self.weather = WeatherService()
        self.flights = FlightService()
        self.hotels = HotelService()
        self.agency = TravelAgencyService()

    def check_trip_updates(self, trip_id: str) -> dict:
        trip = self.memory.get_trip(trip_id)
        if not trip:
            return {"error": f"Trip not found: {trip_id}"}

        destination = trip.get("destination", "Barcelona")
        start_date = trip.get("start_date", "2026-07-10")
        end_date = trip.get("end_date", "2026-07-14")
        departure_code = trip.get("departure_code", "BER")
        arrival_code = trip.get("arrival_code", "BCN")
        adults = int(trip.get("adults", 1))
        rooms = int(trip.get("rooms", 1))

        new_weather = self.weather.get_forecast(destination, start_date, end_date)
        new_flights = self.flights.search(departure_code, arrival_code, adults, start_date, end_date)
        new_hotels = self.hotels.search(destination, start_date, end_date, adults, rooms)

        changes = []
        changes += self._compare("weather", trip.get("weather_summary", ""), new_weather)
        changes += self._compare("flights", trip.get("flight_summary", ""), new_flights)
        changes += self._compare("hotels", trip.get("hotel_summary", ""), new_hotels)

        checked_at = datetime.now().isoformat(timespec="seconds")
        preview_trip = {
            **trip,
            "weather_summary": new_weather,
            "flight_summary": new_flights,
            "hotel_summary": new_hotels,
        }
        alert = {
            "checked_at": checked_at,
            "changes_detected": bool(changes),
            "changes": changes,
            "message": self._message(changes),
            "recommendation": self._recommendation(changes),
            "action_plan": self._action_plan(changes),
            "next_action": self._next_action(changes),
            "risk": self.agency.risk_score(preview_trip),
            "budget": self.agency.estimate_budget(preview_trip),
        }

        alerts = trip.get("alerts", [])
        alerts.append(alert)
        alerts = alerts[-10:]

        updated_trip = self.memory.update_trip(
            trip_id,
            {
                "weather_summary": new_weather,
                "flight_summary": new_flights,
                "hotel_summary": new_hotels,
                "last_checked_at": checked_at,
                "status": "monitored",
                "alerts": alerts,
                "risk": alert["risk"],
                "budget": alert["budget"],
            },
        )

        return {"trip": updated_trip, "alert": alert}

    def _compare(self, label: str, old_value: str, new_value: str) -> list[dict]:
        old_clean = (old_value or "").strip()
        new_clean = (new_value or "").strip()
        if not old_clean:
            return [{"type": label, "status": "new_snapshot", "summary": f"{label.title()} snapshot saved."}]
        if old_clean != new_clean:
            return [{"type": label, "status": "changed", "summary": f"{label.title()} data changed."}]
        return []

    def _message(self, changes: list[dict]) -> str:
        if not changes:
            return "No relevant changes were detected since the last check."
        changed_types = ", ".join(sorted({change["type"] for change in changes}))
        return f"Updates detected for: {changed_types}. The travel file was refreshed."

    def _recommendation(self, changes: list[dict]) -> str:
        if not changes:
            return "No action is needed right now. Keep the current plan."
        changed = {change["type"] for change in changes}
        suggestions = []
        if "weather" in changed:
            suggestions.append("Review the itinerary and keep flexible indoor options ready.")
        if "flights" in changed:
            suggestions.append("Compare the current flight options before final confirmation.")
        if "hotels" in changed:
            suggestions.append("Check whether the saved hotel is still the best value.")
        return " ".join(suggestions)

    def _action_plan(self, changes: list[dict]) -> list[str]:
        if not changes:
            return [
                "Keep the current travel file.",
                "Run the next monitoring check before final confirmation.",
            ]

        changed = {change["type"] for change in changes}
        actions = ["Review the refreshed travel file before sending a final confirmation."]
        if "weather" in changed:
            actions.append("Adjust the daily itinerary and add indoor alternatives if needed.")
        if "flights" in changed:
            actions.append("Compare the new flight options and decide whether the selected flight should change.")
        if "hotels" in changed:
            actions.append("Compare the new hotel options against the saved hotel preference and budget.")
        actions.append("After approval, send an updated email confirmation with the current details.")
        return actions

    def _next_action(self, changes: list[dict]) -> str:
        if not changes:
            return "No user action required."
        changed = {change["type"] for change in changes}
        if "flights" in changed or "hotels" in changed:
            return "Ask the user whether Smart Journey AI should update the selected flight or hotel."
        if "weather" in changed:
            return "Ask the user whether the itinerary should be adjusted for the new weather."
        return "Ask the user whether the refreshed travel file should be confirmed."
