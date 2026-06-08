SAFE_TESTS = [
    ("Weather API", "python src/test_weather_api.py", "Uses live weather data."),
    ("Flight source", "python src/test_flight_source.py", "Checks scraping source without booking anything."),
    ("Hotel source", "python src/test_hotel_source.py", "Checks scraping source without booking anything."),
    ("BlueSky read test", "python src/test_bluesky_source.py", "Reads recent posts only; does not publish."),
]


def main():
    print("Smart Journey AI - API Test Overview")
    print("=" * 42)
    print()
    print("This file no longer runs all integrations automatically.")
    print("Reason: some integrations can trigger real actions such as sending emails,")
    print("starting Google OAuth, or publishing social posts.")
    print()
    print("Use these safe single tests instead:")
    print()

    for name, command, description in SAFE_TESTS:
        print(f"- {name}")
        print(f"  Command: {command}")
        print(f"  Note: {description}")
        print()

    print("Manual integrations for the final presentation:")
    print("- Email sending should be tested only with an explicitly approved recipient.")
    print("- Google Calendar should be tested only when credentials.json is available.")
    print("- BlueSky publishing should be tested only after explicit confirmation.")


if __name__ == "__main__":
    main()
