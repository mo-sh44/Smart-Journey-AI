import json
from datetime import datetime

from services.weather_service import WeatherService
from services.flight_service import FlightService
from services.hotel_service import HotelService
from services.calendar_service import CalendarService
from services.email_service import EmailService
from services.bluesky_service import BlueskyService


class ToolDispatcher:
    def __init__(self):
        self._weather = WeatherService()
        self._flights = FlightService()
        self._hotels = HotelService()
        self._calendar = CalendarService()
        self._email = EmailService()
        self._bluesky = BlueskyService()
        self._handlers = {
            "get_current_date":     self._get_date,
            "get_weather_forecast": self._get_weather,
            "search_flights":       self._search_flights,
            "search_hotels":        self._search_hotels,
            "send_travel_email":    self._send_email,
            "publish_travel_post":  self._publish_post,
            "get_calendar_events":  self._get_calendar,
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
        return self._bluesky.publish_post(args["post_text"])

    def _get_calendar(self, args):
        return json.dumps(self._calendar.get_events(args["start_date"], args["end_date"]), ensure_ascii=False)
