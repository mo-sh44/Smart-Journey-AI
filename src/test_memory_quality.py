from services.memory_service import MemoryService
from services.quality_service import QualityService


def main():
    memory = MemoryService()

    print("Smart Journey AI - Memory and Quality Test")
    print("=" * 50)

    updated_memory = memory.update_user_memory(
        {
            "diet": "vegan",
            "hotel_style": "central hotel or boutique hotel",
            "budget": "medium",
            "interests": ["culture", "cafes", "photography", "beach"],
        }
    )
    print("User memory saved:")
    print(updated_memory)

    trip = memory.save_trip(
        {
            "destination": "Barcelona",
            "start_date": "2026-07-10",
            "end_date": "2026-07-14",
            "weather_summary": "Warm and partly cloudy.",
            "flight_summary": "Option 1: Lufthansa, direct flight.",
            "hotel_summary": "Option 1: W Barcelona.",
            "personalization_notes": "Vegan food, culture, cafes, photography spots.",
        }
    )
    print("\nTrip saved:")
    print(trip)

    quality = QualityService().evaluate_trip_plan(trip)
    print("\nQuality check:")
    print(quality)


if __name__ == "__main__":
    main()
