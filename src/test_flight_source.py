from services.flight_service import FlightService


def main():
    departure = "BER"
    arrival = "BCN"
    passengers = 1
    departure_date = "2026-07-10"
    return_date = "2026-07-14"

    print("Testing flight data source for Smart Journey AI")
    print(f"Route: {departure} to {arrival}")
    print(f"Date range: {departure_date} to {return_date}")
    print()

    result = FlightService().search(departure, arrival, passengers, departure_date, return_date)

    print("Flight source result:")
    print(result)
    print()
    print("Note: This source uses website scraping, so stability is a technical risk.")


if __name__ == "__main__":
    main()
