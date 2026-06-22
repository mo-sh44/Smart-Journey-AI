from services.weather_service import WeatherService


def main():
    departure_city = "Berlin"
    destination_city = "Barcelona"
    start_date = "2026-07-10"
    end_date = "2026-07-14"

    print("Testing Visual Crossing Weather API for Smart Journey AI")
    print(f"Departure city: {departure_city}")
    print(f"Travel destination: {destination_city}")
    print(f"Date range: {start_date} to {end_date}")
    print()

    result = WeatherService().get_forecast(destination_city, start_date, end_date)

    if result and "Fallback data" in result:
        print("Weather API live request failed; fallback data is available.")
        print()
        print(result)
    elif result and "could not be retrieved" not in result:
        print("Weather API works.")
        print()
        print(result)
    else:
        print("Weather API did not return usable data.")
        print(result)


if __name__ == "__main__":
    main()
