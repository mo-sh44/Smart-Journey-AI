class QualityService:
    REQUIRED_PLAN_FIELDS = ("destination", "start_date", "end_date")

    def evaluate_trip_plan(self, plan: dict) -> dict:
        checks = {
            "destination_present": bool(plan.get("destination")),
            "dates_present": bool(plan.get("start_date") and plan.get("end_date")),
            "weather_present": bool(plan.get("weather_summary")),
            "flights_present": bool(plan.get("flight_summary")),
            "hotels_present": bool(plan.get("hotel_summary")),
            "personalization_present": bool(plan.get("personalization_notes")),
        }
        passed = sum(1 for value in checks.values() if value)
        total = len(checks)
        missing = [name for name, value in checks.items() if not value]
        return {
            "score": f"{passed}/{total}",
            "passed": passed,
            "total": total,
            "checks": checks,
            "missing": missing,
            "recommendation": self._recommendation(missing),
        }

    def _recommendation(self, missing: list[str]) -> str:
        if not missing:
            return "The trip plan is complete enough for a user recommendation."
        if "weather_present" in missing:
            return "Weather data should be checked before confirming the trip."
        if "flights_present" in missing or "hotels_present" in missing:
            return "Flight and hotel options should be added before final confirmation."
        return "The plan is usable, but personalization can still be improved."
