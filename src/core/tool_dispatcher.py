import json
from datetime import datetime

from services.weather_service import WeatherService
from services.flight_service import FlightService
from services.hotel_service import HotelService
from services.email_service import EmailService
from services.memory_service import MemoryService
from services.monitoring_service import MonitoringService
from services.quality_service import QualityService
from services.travel_agency_service import TravelAgencyService


class ToolDispatcher:
    def __init__(self):
        self._weather = WeatherService()
        self._flights = FlightService()
        self._hotels = HotelService()
        self._calendar = None
        self._email = EmailService()
        self._bluesky = None
        self._memory = MemoryService()
        self._monitoring = MonitoringService()
        self._quality = QualityService()
        self._agency = TravelAgencyService()
        self._handlers = {
            "get_current_date":     self._get_date,
            "get_weather_forecast": self._get_weather,
            "search_flights":       self._search_flights,
            "search_hotels":        self._search_hotels,
            "send_travel_email":    self._send_email,
            "publish_travel_post":  self._publish_post,
            "get_calendar_events":  self._get_calendar,
            "get_user_memory":      self._get_user_memory,
            "save_user_memory":     self._save_user_memory,
            "get_saved_trips":      self._get_saved_trips,
            "save_trip_plan":       self._save_trip_plan,
            "update_trip_weather":  self._update_trip_weather,
            "run_quality_check":    self._run_quality_check,
            "check_trip_updates":   self._check_trip_updates,
            "estimate_trip_budget": self._estimate_trip_budget,
            "create_packing_list":  self._create_packing_list,
            "calculate_risk_score": self._calculate_risk_score,
        }

    def dispatch(self, function_name: str, arguments: dict) -> str:
        handler = self._handlers.get(function_name)
        if handler is None:
            return json.dumps({"error": f"Unknown tool: '{function_name}'"})
        try:
            result = handler(arguments)
            return result if isinstance(result, str) else json.dumps(result)
        except Exception as exc:
            return json.dumps({"error": str(exc)})

    def _get_date(self, _args):
        return datetime.now().strftime("%Y-%m-%d")

    def _get_weather(self, args):
        return self._weather.get_forecast(args["location"], args["start_date"], args["end_date"])

    def _search_flights(self, args):
        return self._flights.search(
            departure_code=args["departure_code"],
            arrival_code=args["arrival_code"],
            passengers=int(args["passengers"]),
            departure_date=args["departure_date"],
            return_date=args["return_date"],
        )

    def _search_hotels(self, args):
        return self._hotels.search(
            city=args["city"],
            checkin_date=args["checkin_date"],
            checkout_date=args["checkout_date"],
            adults=int(args["adults"]),
            rooms=int(args.get("rooms", 1)),
        )

    def _send_email(self, args):
        return self._email.send_travel_confirmation(
            recipient=args["recipient_email"],
            subject=args["subject"],
            body=args["body"],
            event_details=args["calendar_event"],
        )

    def _publish_post(self, args):
        if self._bluesky is None:
            from services.bluesky_service import BlueskyService
            self._bluesky = BlueskyService()
        return self._bluesky.publish_post(args["post_text"])

    def _get_calendar(self, args):
        if self._calendar is None:
            from services.calendar_service import CalendarService
            self._calendar = CalendarService()
        return json.dumps(self._calendar.get_events(args["start_date"], args["end_date"]), ensure_ascii=False)

    def _get_user_memory(self, _args):
        return json.dumps(self._memory.get_user_memory(), ensure_ascii=False)

    def _save_user_memory(self, args):
        return json.dumps(self._memory.update_user_memory(args["preferences"]), ensure_ascii=False)

    def _get_saved_trips(self, _args):
        return json.dumps(self._memory.get_saved_trips(), ensure_ascii=False)

    def _save_trip_plan(self, args):
        return json.dumps(self._memory.save_trip(args["trip"]), ensure_ascii=False)

    def _update_trip_weather(self, args):
        return json.dumps(
            self._memory.update_trip_weather(args["trip_id"], args["weather_summary"]),
            ensure_ascii=False,
        )

    def _run_quality_check(self, args):
        return json.dumps(self._quality.evaluate_trip_plan(args["plan"]), ensure_ascii=False)

    def _check_trip_updates(self, args):
        return json.dumps(self._monitoring.check_trip_updates(args["trip_id"]), ensure_ascii=False)

    def _estimate_trip_budget(self, args):
        return json.dumps(self._agency.estimate_budget(args["trip"]), ensure_ascii=False)

    def _create_packing_list(self, args):
        return json.dumps(
            self._agency.create_packing_list(args["trip"], args.get("preferences", {})),
            ensure_ascii=False,
        )

    def _calculate_risk_score(self, args):
        return json.dumps(self._agency.risk_score(args["trip"]), ensure_ascii=False)
