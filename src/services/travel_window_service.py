from datetime import datetime, timedelta

from services.calendar_service import CalendarService
from services.weather_service import WeatherService


class TravelWindowService:
    def __init__(self):
        self.calendar = CalendarService()
        self.weather = WeatherService()

    def find_best_windows(
        self,
        destination: str,
        earliest_date: str,
        latest_date: str,
        duration_days: int,
        max_results: int = 3,
    ) -> dict:
        start = datetime.strptime(earliest_date, "%Y-%m-%d").date()
        end = datetime.strptime(latest_date, "%Y-%m-%d").date()
        duration = max(int(duration_days), 1)
        calendar_warning = None
        try:
            calendar_data = self.calendar.get_events(earliest_date, latest_date)
        except Exception as exc:
            calendar_data = {"personal": [], "holidays": []}
            calendar_warning = (
                "Calendar access was not available, so the agent used an empty-calendar fallback. "
                f"Reason: {type(exc).__name__}"
            )

        if "error" in calendar_data:
            calendar_warning = "Calendar returned an error, so the agent used an empty-calendar fallback."
            calendar_data = {"personal": [], "holidays": []}

        busy_dates = self._collect_dates(calendar_data.get("personal", []))
        holiday_dates = self._collect_dates(calendar_data.get("holidays", []))
        candidates = []

        current = start
        while current + timedelta(days=duration - 1) <= end:
            window_days = [current + timedelta(days=offset) for offset in range(duration)]
            if not any(day in busy_dates for day in window_days):
                candidates.append(
                    self._score_window(current, duration, window_days, holiday_dates)
                )
            current += timedelta(days=1)

        candidates = sorted(candidates, key=lambda item: item["score"], reverse=True)
        top_candidates = candidates[:max_results]

        for candidate in top_candidates:
            candidate["weather_summary"] = self.weather.get_forecast(
                destination,
                candidate["start_date"],
                candidate["end_date"],
            )
            candidate["recommendation"] = self._recommendation(candidate)

        return {
            "destination": destination,
            "earliest_date": earliest_date,
            "latest_date": latest_date,
            "duration_days": duration,
            "calendar_summary": {
                "busy_days": len(busy_dates),
                "holiday_days": len(holiday_dates),
                "warning": calendar_warning,
            },
            "best_windows": top_candidates,
            "message": "Best travel windows were calculated from calendar availability, holidays, weekends, and weather.",
        }

    def _score_window(self, start, duration, window_days, holiday_dates):
        weekend_days = sum(1 for day in window_days if day.weekday() >= 5)
        holidays_inside = sum(1 for day in window_days if day in holiday_dates)
        adjacent_holidays = sum(
            1
            for day in [start - timedelta(days=1), start + timedelta(days=duration)]
            if day in holiday_dates
        )
        score = 50 + weekend_days * 5 + holidays_inside * 10 + adjacent_holidays * 6
        end = start + timedelta(days=duration - 1)
        return {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "score": score,
            "weekend_days": weekend_days,
            "holidays_inside": holidays_inside,
            "adjacent_holidays": adjacent_holidays,
            "reason": self._reason(weekend_days, holidays_inside, adjacent_holidays),
        }

    def _reason(self, weekend_days, holidays_inside, adjacent_holidays):
        reasons = ["No personal calendar conflict was found."]
        if weekend_days:
            reasons.append(f"{weekend_days} weekend day(s) reduce required vacation days.")
        if holidays_inside:
            reasons.append(f"{holidays_inside} public holiday day(s) are inside the window.")
        if adjacent_holidays:
            reasons.append("A public holiday is close to this window.")
        return " ".join(reasons)

    def _recommendation(self, candidate):
        weather = candidate.get("weather_summary", "").lower()
        if "rain" in weather:
            return "Good calendar fit, but keep indoor activities ready because rain is possible."
        if "35" in weather or "36" in weather or "hot" in weather:
            return "Good calendar fit, but plan sightseeing in the morning because it may be very warm."
        return "Strong option: free calendar window and acceptable weather for travel planning."

    def _collect_dates(self, events):
        dates = set()
        for event in events:
            raw_date = event.get("date", "")
            if not raw_date:
                continue
            try:
                dates.add(datetime.fromisoformat(raw_date.replace("Z", "+00:00")).date())
            except ValueError:
                try:
                    dates.add(datetime.strptime(raw_date[:10], "%Y-%m-%d").date())
                except ValueError:
                    continue
        return dates
