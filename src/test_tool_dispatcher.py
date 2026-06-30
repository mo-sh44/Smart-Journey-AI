from core.tool_dispatcher import ToolDispatcher


def show_result(title, result):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(result)


def main():
    dispatcher = ToolDispatcher()

    print("Smart Journey AI - Tool Dispatcher Test")
    print("This test uses the same tool layer as the OpenAI Assistant.")

    show_result(
        "Current date",
        dispatcher.dispatch("get_current_date", {}),
    )

    show_result(
        "Weather tool",
        dispatcher.dispatch(
            "get_weather_forecast",
            {
                "location": "Barcelona",
                "start_date": "2026-07-10",
                "end_date": "2026-07-14",
            },
        ),
    )

    show_result(
        "Flight tool",
        dispatcher.dispatch(
            "search_flights",
            {
                "departure_code": "BER",
                "arrival_code": "BCN",
                "passengers": 1,
                "departure_date": "2026-07-10",
                "return_date": "2026-07-14",
            },
        ),
    )

    show_result(
        "Hotel tool",
        dispatcher.dispatch(
            "search_hotels",
            {
                "city": "Barcelona",
                "checkin_date": "2026-07-10",
                "checkout_date": "2026-07-14",
                "adults": 1,
                "rooms": 1,
            },
        ),
    )

    show_result(
        "User memory tool",
        dispatcher.dispatch(
            "save_user_memory",
            {
                "preferences": {
                    "diet": "vegan",
                    "hotel_style": "central hotel",
                    "budget": "medium",
                    "interests": ["culture", "cafes", "photography"],
                }
            },
        ),
    )

    show_result(
        "Quality check tool",
        dispatcher.dispatch(
            "run_quality_check",
            {
                "plan": {
                    "destination": "Barcelona",
                    "start_date": "2026-07-10",
                    "end_date": "2026-07-14",
                    "weather_summary": "Warm and partly cloudy.",
                    "flight_summary": "Option 1: Lufthansa.",
                    "hotel_summary": "Option 1: W Barcelona.",
                    "personalization_notes": "Vegan food, culture, cafes, photography.",
                }
            },
        ),
    )

    trip = {
        "destination": "Barcelona",
        "departure_code": "BER",
        "arrival_code": "BCN",
        "start_date": "2026-07-10",
        "end_date": "2026-07-14",
        "adults": 1,
        "rooms": 1,
        "weather_summary": "Warm and partly cloudy.",
        "flight_summary": "Option 1: Lufthansa | Price: 176 EUR | Outbound: 2h 15m (direct)",
        "hotel_summary": "Hotel 1: W Barcelona | Preis: 223 EUR/Nacht",
        "personalization_notes": "Vegan food, culture, cafes, photography.",
        "daily_budget": 60,
    }

    saved_trip = dispatcher.dispatch("save_trip_plan", {"trip": trip})
    show_result("Save travel file tool", saved_trip)

    show_result(
        "Budget tool",
        dispatcher.dispatch("estimate_trip_budget", {"trip": trip}),
    )

    show_result(
        "Packing list tool",
        dispatcher.dispatch(
            "create_packing_list",
            {
                "trip": trip,
                "preferences": {
                    "diet": "vegan",
                    "interests": ["culture", "cafes", "photography"],
                },
            },
        ),
    )

    show_result(
        "Risk score tool",
        dispatcher.dispatch("calculate_risk_score", {"trip": trip}),
    )

    import json
    trip_id = json.loads(saved_trip)["id"]
    show_result(
        "Monitoring tool",
        dispatcher.dispatch("check_trip_updates", {"trip_id": trip_id}),
    )


if __name__ == "__main__":
    main()
