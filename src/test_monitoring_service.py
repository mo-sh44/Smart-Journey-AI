from services.memory_service import MemoryService
from services.monitoring_service import MonitoringService


def main():
    memory = MemoryService()
    trips = memory.get_saved_trips()
    if not trips:
        trip = memory.save_trip(
            {
                "destination": "Barcelona",
                "departure_code": "BER",
                "arrival_code": "BCN",
                "start_date": "2026-07-10",
                "end_date": "2026-07-14",
                "adults": 1,
                "rooms": 1,
                "weather_summary": "",
                "flight_summary": "",
                "hotel_summary": "",
                "personalization_notes": "Demo user likes vegan food, culture, cafes, and photography.",
            }
        )
    else:
        trip = trips[-1]

    print("Smart Journey AI - Monitoring Test")
    print("=" * 50)
    print(f"Checking trip: {trip.get('id')} -> {trip.get('destination')}")
    result = MonitoringService().check_trip_updates(trip["id"])
    print(result["alert"])


if __name__ == "__main__":
    main()
