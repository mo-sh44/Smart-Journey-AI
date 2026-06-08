from services.hotel_service import HotelService


def main():
    city = "Barcelona"
    checkin_date = "2026-07-10"
    checkout_date = "2026-07-14"
    adults = 1
    rooms = 1

    print("Testing hotel data source for Smart Journey AI")
    print(f"City: {city}")
    print(f"Date range: {checkin_date} to {checkout_date}")
    print()

    result = HotelService().search(city, checkin_date, checkout_date, adults, rooms)

    print("Hotel source result:")
    print(result)
    print()
    print("Note: This source uses website scraping, so stability is a technical risk.")


if __name__ == "__main__":
    main()
