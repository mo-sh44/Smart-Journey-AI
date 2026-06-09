from pathlib import Path

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
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed.")
        print("Run: pip install -r requirements.txt")
        print("Run: python -m playwright install chromium")
        return

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=service.HEADERS["User-Agent"],
            locale="de-DE",
            extra_http_headers={"Accept-Language": "de-DE,de;q=0.9,en;q=0.8"},
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(15000)

        title = page.title()
        html = page.content()
        screenshot_path = output_dir / "swoodoo_flight_debug.png"
        html_path = output_dir / "swoodoo_flight_debug.html"

        page.screenshot(path=str(screenshot_path), full_page=True)
        html_path.write_text(html, encoding="utf-8")

        browser.close()

    print(f"Page title: {title}")
    print(f"HTML saved: {html_path}")
    print(f"Screenshot saved: {screenshot_path}")
    print()

    parsed = service._parse(html)
    if parsed:
        print("Parser found flight data:")
        print(parsed)
    else:
        print("Parser did not find flight data.")
        print("Next step: inspect the screenshot/HTML to see whether Swoodoo blocks the page or changed selectors.")


if __name__ == "__main__":
    main()
