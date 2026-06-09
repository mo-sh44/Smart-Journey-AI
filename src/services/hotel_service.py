import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode


class HotelService:
    BASE_URL = "https://www.booking.com/searchresults.de.html"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
    }

    def search(self, city: str, checkin_date: str, checkout_date: str,
               adults: int, rooms: int = 1) -> str:
        url = self._build_url(city, checkin_date, checkout_date, adults, rooms)
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=15)
            if response.status_code == 200:
                result = self._parse(response.text)
                if result:
                    return result

            browser_result = self._search_with_browser(url)
            if browser_result:
                return browser_result

            return f"Hotel search failed (HTTP {response.status_code})."
        except requests.RequestException as exc:
            browser_result = self._search_with_browser(url)
            if browser_result:
                return browser_result
            return f"Hotel search unavailable: {type(exc).__name__}"

    def _build_url(self, city: str, checkin_date: str, checkout_date: str,
                   adults: int, rooms: int = 1) -> str:
        params = {
            "ss": city,
            "checkin": checkin_date,
            "checkout": checkout_date,
            "group_adults": adults,
            "no_rooms": rooms,
            "lang": "de",
        }
        return f"{self.BASE_URL}?{urlencode(params)}"

    def _parse(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", {"data-testid": "property-card"}, limit=5)
        if not cards:
            return "No hotels found."
        results = []
        for i, card in enumerate(cards, start=1):
            name = card.find("div", {"data-testid": "title"})
            price = card.find("span", {"data-testid": "price-and-discounted-price", "aria-hidden": "true"})
            rating = card.find("span", {"data-testid": "review-score", "aria-hidden": "true"})
            distance = card.find("span", {"data-testid": "distance"})
            results.append(
                f"Hotel {i}: {name.text.strip() if name else 'N/A'} | "
                f"Price: {price.text.strip() if price else 'N/A'} | "
                f"Rating: {rating.text.strip() if rating else 'N/A'} | "
                f"Distance: {distance.text.strip() if distance else 'N/A'}"
            )
        return "\n".join(results)

    def _search_with_browser(self, url: str) -> str:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return (
                "Hotel browser search requires Playwright. "
                "Run: pip install -r requirements.txt && python -m playwright install chromium"
            )

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.HEADERS["User-Agent"],
                    locale="de-DE",
                    extra_http_headers={"Accept-Language": self.HEADERS["Accept-Language"]},
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(8000)
                html = page.content()
                browser.close()
            return self._parse(html)
        except Exception as exc:
            return f"Hotel browser search unavailable: {type(exc).__name__}"
