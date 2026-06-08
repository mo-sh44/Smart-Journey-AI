import requests
from bs4 import BeautifulSoup


class HotelService:
    BASE_URL = "https://www.booking.com/searchresults.en-gb.html"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def search(self, city: str, checkin_date: str, checkout_date: str,
               adults: int, rooms: int = 1) -> str:
        url = f"{self.BASE_URL}?ss={city}&checkin={checkin_date}&checkout={checkout_date}&group_adults={adults}&no_rooms={rooms}"
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=15)
            if response.status_code != 200:
                return f"Hotel search failed (HTTP {response.status_code})."
            return self._parse(response.text)
        except requests.RequestException as exc:
            return f"Hotel search unavailable: {exc}"

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
