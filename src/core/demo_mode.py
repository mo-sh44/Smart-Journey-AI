import re

from services.weather_service import WeatherService


def extract_trip_details(prompt: str):
    departure = "Berlin"
    destination = "Barcelona"
    start_date = "2026-07-10"
    end_date = "2026-07-14"
    trip_type = "city"

    prompt_lower = prompt.lower()
    if "city break" in prompt_lower:
        destination = "Lisbon"
        start_date = "2026-08-06"
        end_date = "2026-08-10"
        trip_type = "city"
    elif "beach" in prompt_lower:
        destination = "Mallorca"
        start_date = "2026-07-20"
        end_date = "2026-07-26"
        trip_type = "beach"
    elif "winter" in prompt_lower or "alps" in prompt_lower:
        destination = "Innsbruck"
        start_date = "2026-12-12"
        end_date = "2026-12-18"
        trip_type = "winter"

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

    return departure, destination, start_date, end_date, trip_type


def _convert_german_date(date_text: str) -> str:
    day, month, year = date_text.split(".")
    return f"{year}-{month}-{day}"


def create_demo_travel_plan(prompt: str) -> str:
    departure, destination, start_date, end_date, trip_type = extract_trip_details(prompt)
    weather = WeatherService().get_forecast(destination, start_date, end_date)

    if not weather or "could not be retrieved" in weather:
        weather = "No live weather data could be retrieved. The app can continue with fallback data for the demo."
    else:
        weather = weather.replace("\n", "\n\n")

    assessment = _build_assessment(trip_type)
    itinerary = _build_itinerary(departure, destination, trip_type)

    return f"""
### Demo-Reisevorschlag: {departure} nach {destination}

**Zeitraum:** {start_date} bis {end_date}

**Wetter am Reiseziel**

{weather}

**Kurzbewertung**

{assessment}

**Vorschlag fuer die Reiseplanung**

{itinerary}

**MVP-Hinweis**

Dieser Demo-Modus nutzt echte Wetterdaten. Der OpenAI Assistant ist eingerichtet, kann aber bei API-Quota- oder Billing-Problemen durch diesen stabilen Fallback ersetzt werden.
""".strip()


def _build_assessment(trip_type: str) -> str:
    if trip_type == "beach":
        return "Das Wetter wird fuer Strandaktivitaeten geprueft. Wichtig sind warme Temperaturen, wenig Regen und ausreichend stabile Bedingungen fuer entspannte Tage am Meer."
    if trip_type == "winter":
        return "Bei einer Winterreise sind Wetterbedingungen besonders wichtig. Die Planung sollte flexibel bleiben, weil Schnee, Kaelte und Sichtverhaeltnisse Ausfluege stark beeinflussen koennen."
    return "Das Wetter wirkt fuer eine Staedtereise gut geeignet. Angenehme Temperaturen und teilweise bewoelktes Wetter sind fuer Sightseeing oft praktischer als extreme Hitze."


def _build_itinerary(departure: str, destination: str, trip_type: str) -> str:
    if trip_type == "beach":
        return "\n".join([
            f"- **Tag 1:** Anreise von {departure} nach {destination}, Check-in und kurzer Spaziergang am Strand.",
            "- **Tag 2:** Strandtag mit leichter Aktivitaet, z.B. Promenade, Cafes oder Sonnenuntergang.",
            "- **Tag 3:** Ausflug zu einem Aussichtspunkt oder einer Kueste in der Umgebung.",
            "- **Tag 4:** Freier Tag fuer Erholung, lokale Kueche und flexible Aktivitaeten je nach Wetter.",
            f"- **Letzter Tag:** Rueckreise nach {departure}.",
        ])
    if trip_type == "winter":
        return "\n".join([
            f"- **Tag 1:** Anreise von {departure} nach {destination}, Check-in und Orientierung vor Ort.",
            "- **Tag 2:** Winteraktivitaet wie Skigebiet, Bergbahn oder Spaziergang in der Altstadt.",
            "- **Tag 3:** Wetterabhaengiger Ausflug in die Berge oder Besuch eines Museums bei schlechtem Wetter.",
            "- **Tag 4:** Entspannter Tag mit regionalem Essen und Vorbereitung der Rueckreise.",
            f"- **Letzter Tag:** Rueckreise nach {departure}.",
        ])
    return "\n".join([
        f"- **Tag 1:** Anreise von {departure} nach {destination}, Check-in und entspannter Abend in der Innenstadt.",
        "- **Tag 2:** Stadterkundung mit bekannten Sehenswuerdigkeiten und Spaziergang durch zentrale Viertel.",
        "- **Tag 3:** Aktivitaeten passend zum Wetter, z.B. Park, Museum oder lokale Kultur.",
        "- **Tag 4:** Freier Tag fuer persoenliche Interessen und lokale Restaurants.",
        f"- **Letzter Tag:** Rueckreise nach {departure}.",
    ])
