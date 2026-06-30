import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2] / "data"
MEMORY_FILE = DATA_DIR / "user_memory.json"
TRIPS_FILE = DATA_DIR / "saved_trips.json"


class MemoryService:
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)

    def get_user_memory(self) -> dict:
        data = self._read_json(MEMORY_FILE, self._default_memory())
        return data

    def update_user_memory(self, preferences: dict) -> dict:
        memory = self.get_user_memory()
        stored_preferences = memory.setdefault("preferences", {})
        for key, value in preferences.items():
            if value not in ("", None, [], {}):
                stored_preferences[key] = value
        memory["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self._write_json(MEMORY_FILE, memory)
        return memory

    def get_saved_trips(self) -> list[dict]:
        return self._read_json(TRIPS_FILE, [])

    def get_trip(self, trip_id: str) -> dict | None:
        for trip in self.get_saved_trips():
            if trip.get("id") == trip_id:
                return trip
        return None

    def save_trip(self, trip: dict) -> dict:
        trips = self.get_saved_trips()
        trip_id = trip.get("id") or f"trip-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        saved_trip = {
            "id": trip_id,
            "status": trip.get("status", "planned"),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            **trip,
            "id": trip_id,
        }
        trips = [existing for existing in trips if existing.get("id") != trip_id]
        trips.append(saved_trip)
        self._write_json(TRIPS_FILE, trips)
        return saved_trip

    def update_trip(self, trip_id: str, updates: dict) -> dict:
        trips = self.get_saved_trips()
        for trip in trips:
            if trip.get("id") == trip_id:
                trip.update(updates)
                trip["updated_at"] = datetime.now().isoformat(timespec="seconds")
                self._write_json(TRIPS_FILE, trips)
                return trip
        return {"error": f"Trip not found: {trip_id}"}

    def update_trip_weather(self, trip_id: str, weather_summary: str) -> dict:
        trips = self.get_saved_trips()
        for trip in trips:
            if trip.get("id") == trip_id:
                old_weather = trip.get("weather_summary", "")
                trip["previous_weather_summary"] = old_weather
                trip["weather_summary"] = weather_summary
                trip["updated_at"] = datetime.now().isoformat(timespec="seconds")
                trip["status"] = "updated"
                self._write_json(TRIPS_FILE, trips)
                return {
                    "trip": trip,
                    "change_detected": old_weather.strip() != weather_summary.strip(),
                    "old_weather": old_weather,
                    "new_weather": weather_summary,
                }
        return {"error": f"Trip not found: {trip_id}"}

    def _default_memory(self) -> dict:
        return {
            "profile_name": "Demo User",
            "preferences": {
                "diet": "",
                "hotel_style": "",
                "budget": "",
                "interests": [],
                "mobility": "",
            },
            "updated_at": None,
        }

    def _read_json(self, path: Path, default):
        if not path.exists():
            return default
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return default

    def _write_json(self, path: Path, data) -> None:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
