from services.travel_window_service import TravelWindowService


def main():
    print("Smart Journey AI - Best Travel Window Test")
    print("=" * 50)
    print("Destination: Barcelona")
    print("Search range: 2026-08-01 to 2026-08-31")
    print("Duration: 5 days")
    print()

    result = TravelWindowService().find_best_windows(
        destination="Barcelona",
        earliest_date="2026-08-01",
        latest_date="2026-08-31",
        duration_days=5,
        max_results=3,
    )

    if "error" in result:
        print("Travel window search failed:")
        print(result.get("message", result["error"]))
        return

    print(result["message"])
    print()
    for index, window in enumerate(result["best_windows"], start=1):
        print(f"Option {index}: {window['start_date']} to {window['end_date']}")
        print(f"Score: {window['score']}")
        print(f"Reason: {window['reason']}")
        print(f"Weather: {window['weather_summary']}")
        print(f"Recommendation: {window['recommendation']}")
        print()


if __name__ == "__main__":
    main()
