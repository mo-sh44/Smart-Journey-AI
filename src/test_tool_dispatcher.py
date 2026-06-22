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


if __name__ == "__main__":
    main()
