from pathlib import Path

from services.calendar_service import CalendarService


def main():
    print("Smart Journey AI - Calendar Test")
    print("=" * 50)

    service = CalendarService()
    credentials = Path(service.credentials_path)

    if not credentials.exists():
        print("Google Calendar credentials not found.")
        print(f"Expected file: {credentials}")
        print()
        print("Status: Calendar integration is prepared in code,")
        print("but live access needs data/credentials.json from Google Cloud.")
        return

    print("Credentials found. Reading events...")
    result = service.get_events("2026-07-01", "2026-07-31")
    print(result)


if __name__ == "__main__":
    main()
