import re

from services.weather_service import WeatherService


def extract_trip_details(prompt: str):
    departure = "Berlin"
    destination = "Barcelona"
    start_date = "2026-07-10"
    end_date = "2026-07-14"

    route_match = re.search(
        r"von\s+([A-Za-zÄÖÜäöüß\s]+?)\s+nach\s+([A-Za-zÄÖÜäöüß\s]+?)(?:\s+vom|\s+von|\s+am|\.|,|$)",
        prompt,
        re.IGNORECASE,
    )
    if route_match:
        departure = route_match.group(1).strip()
        destination = route_match.group(2).strip()

    dates = re.findall(r"\d{2}\.\d{2}\.\d{4}", prompt)
    if len(dates) >= 2:
        start_date = _convert_german_date(dates[0])
        end_date = _convert_german_date(dates[1])

    return departure, destination, start_date, end_date


def _convert_german_date(date_text: str) -> str:
    day, month, year = date_text.split(".")
    return f"{year}-{month}-{day}"


def create_demo_travel_plan(prompt: str) -> str:
    departure, destination, start_date, end_date = extract_trip_details(prompt)
    weather = WeatherService().get_forecast(destination, start_date, end_date)

    if not weather or "could not be retrieved" in weather:
        weather = "No live weather data could be retrieved. The app can continue with fallback data for the demo."
    else:
        weather = weather.replace("\n", "\n\n")

    return f"""
### Demo-Reisevorschlag: {departure} nach {destination}

**Zeitraum:** {start_date} bis {end_date}

**Wetter am Reiseziel**

{weather}

**Kurzbewertung**

Das Wetter wirkt fuer eine Staedtereise gut geeignet. Die Temperaturen liegen im angenehmen Sommerbereich, und teilweise bewoelktes Wetter ist fuer Sightseeing oft praktischer als extreme Hitze.

**Vorschlag fuer die Reiseplanung**

- **Tag 1:** Anreise von {departure} nach {destination}, Check-in und entspannter Abend in der Innenstadt.
- **Tag 2:** Stadterkundung mit bekannten Sehenswuerdigkeiten und Spaziergang durch zentrale Viertel.
- **Tag 3:** Aktivitaeten passend zum Wetter, z.B. Strand, Park oder kulturelle Besichtigungen.
- **Tag 4:** Freier Tag fuer persoenliche Interessen und lokale Restaurants.
- **Tag 5:** Rueckreise nach {departure}.

**MVP-Hinweis**

Dieser Demo-Modus nutzt echte Wetterdaten. Der OpenAI Assistant ist eingerichtet, kann aber bei API-Quota- oder Billing-Problemen durch diesen stabilen Fallback ersetzt werden.
""".strip()
