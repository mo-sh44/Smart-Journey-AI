import os

import requests
from dotenv import load_dotenv

load_dotenv()


class LocalAIService:
    def __init__(self):
        self.base_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434")
        self.model = os.getenv("LOCAL_LLM_MODEL", "gemma3:4b")

    def generate_travel_plan(self, user_prompt: str, trip_details: dict, weather: str) -> str:
        prompt = self._build_prompt(user_prompt, trip_details, weather)
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.4,
                    },
                },
                timeout=90,
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("response", "").strip()
            if answer:
                return answer
            return "Local AI returned an empty response."
        except requests.RequestException as error:
            return (
                "Local AI could not be reached. "
                f"Please make sure Ollama is running and the model '{self.model}' is installed. "
                f"Error: {type(error).__name__}"
            )

    def _build_prompt(self, user_prompt: str, trip_details: dict, weather: str) -> str:
        return f"""
You are Smart Journey AI, an AI-powered travel planning assistant.

Create a personalized travel proposal in German.
Use the user's request, the extracted trip details, and the live weather data.
Do not pretend that flights or hotels were booked.
If flight or hotel live data is missing, mention that these sources are planned as next tool integrations.

User request:
{user_prompt}

Extracted trip details:
- Departure: {trip_details["departure"]}
- Destination: {trip_details["destination"]}
- Weather lookup location: {trip_details["weather_location"]}
- Start date: {trip_details["start_date"]}
- End date: {trip_details["end_date"]}
- Trip type: {trip_details["trip_type"]}

Live weather data:
{weather}

Output format:
### Reisevorschlag: [departure] nach [destination]
**Zeitraum:** ...
**Wetterbewertung:** ...
**Empfohlener Plan:** bullet list by day
**Naechste Schritte:** mention flights/hotels/calendar as tool integrations
""".strip()
