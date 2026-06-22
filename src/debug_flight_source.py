from pathlib import Path

import requests

from services.flight_service import FlightService


def main():
    service = FlightService()
    url = service._build_url("BER", "BCN", 1, "2026-07-10", "2026-07-14")
    output_dir = Path("debug")
    output_dir.mkdir(exist_ok=True)

    print("Debugging Swoodoo flight source")
    print(f"URL: {url}")
    print()

    try:
        response = requests.get(url, headers=service.HEADERS, timeout=15)
    except requests.RequestException as error:
        print(f"Request failed: {type(error).__name__}")
        return

    html = response.text
    html_path = output_dir / "swoodoo_flight_debug.html"
    html_path.write_text(html, encoding="utf-8")

    print(f"HTTP status: {response.status_code}")
    print(f"HTML saved: {html_path}")
    print()

    parsed = service._parse(html)
    if parsed:
        print("Parser found flight data:")
        print(parsed)
    else:
        print("Parser did not find flight data.")
        print("Next step: inspect the HTML to see whether Swoodoo blocks the page or changed selectors.")


if __name__ == "__main__":
    main()
