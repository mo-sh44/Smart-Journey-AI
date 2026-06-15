import os
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherService:
    BASE_URL = (
        "https://weather.visualcrossing.com"
        "/VisualCrossingWebServices/rest/services/timeline"
    )

    def __init__(self):
        self.api_key = os.getenv("VISUAL_CROSSING_API_KEY")

    def get_forecast(self, location: str, start_date: str, end_date: str) -> str:
        if not self.api_key:
            return "Weather data could not be retrieved: missing VISUAL_CROSSING_API_KEY."

        url = f"{self.BASE_URL}/{location}/{start_date}/{end_date}"
        params = {
            "unitGroup": "metric",
            "include": "days",
            "key": self.api_key,
            "contentType": "json",
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            lines = []
            for day in data.get("days", []):
                lines.append(
                    f"{day['datetime']}: {day['tempmin']}°C – {day['tempmax']}°C, {day['conditions']}"
                )
            return "\n".join(lines) if lines else "No weather data available."
        except requests.RequestException as exc:
            return f"Weather data could not be retrieved: {type(exc).__name__}"
