import re


class TravelAgencyService:
    def estimate_budget(self, trip: dict) -> dict:
        nights = self._estimate_nights(trip)
        flight_price = self._first_price(trip.get("flight_summary", ""))
        hotel_price = self._first_price(trip.get("hotel_summary", ""))
        daily_budget = int(trip.get("daily_budget", 55))

        total = 0
        parts = {}
        if flight_price:
            parts["flight"] = flight_price
            total += flight_price
        if hotel_price:
            parts["hotel"] = hotel_price * max(nights, 1)
            total += parts["hotel"]
        parts["daily_costs"] = daily_budget * max(nights, 1)
        total += parts["daily_costs"]

        return {
            "estimated_total": total,
            "currency": "EUR",
            "nights": nights,
            "parts": parts,
            "note": "This is an MVP estimate based on available flight, hotel, and daily-cost data.",
        }

    def create_packing_list(self, trip: dict, preferences: dict) -> list[str]:
        weather = (trip.get("weather_summary") or "").lower()
        interests = preferences.get("interests", [])
        if isinstance(interests, str):
            interests = [interests]
        items = [
            "Passport or ID",
            "Phone charger and power bank",
            "Comfortable walking shoes",
            "Travel confirmation and insurance documents",
        ]
        if "35" in weather or "warm" in weather or "hot" in weather:
            items += ["Sunscreen", "Light clothes", "Reusable water bottle", "Sunglasses"]
        if "rain" in weather:
            items += ["Light rain jacket", "Compact umbrella"]
        if any("photo" in item.lower() for item in interests):
            items += ["Camera or phone lens", "Extra storage or cloud backup"]
        if preferences.get("diet"):
            items += [f"Saved food preference: {preferences['diet']}", "List of suitable restaurants"]
        return items

    def risk_score(self, trip: dict) -> dict:
        score = 0
        reasons = []
        weather = trip.get("weather_summary", "")
        if "failed" in weather.lower() or "could not" in weather.lower():
            score += 2
            reasons.append("Weather data is not fully reliable.")
        if not trip.get("flight_summary"):
            score += 2
            reasons.append("No flight option stored.")
        if not trip.get("hotel_summary"):
            score += 2
            reasons.append("No hotel option stored.")
        alerts = trip.get("alerts", [])
        if alerts and alerts[-1].get("changes_detected"):
            score += 1
            reasons.append("Recent monitoring detected changes.")

        level = "low"
        if score >= 4:
            level = "high"
        elif score >= 2:
            level = "medium"

        return {
            "level": level,
            "score": score,
            "reasons": reasons or ["No major risk detected."],
        }

    def _first_price(self, text: str) -> int:
        matches = re.findall(r"(\d+)\s*(?:€|EUR)", text or "")
        return int(matches[0]) if matches else 0

    def _estimate_nights(self, trip: dict) -> int:
        try:
            from datetime import datetime
            start = datetime.strptime(trip.get("start_date", ""), "%Y-%m-%d")
            end = datetime.strptime(trip.get("end_date", ""), "%Y-%m-%d")
            return max((end - start).days, 1)
        except ValueError:
            return int(trip.get("nights", 4))
