import asyncio
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from services.fallback_data import FLIGHTS_BER_BCN


class FlightService:
    BASE_URL = "https://www.swoodoo.com/flights"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    MAX_RETRIES = 2

    def search(self, departure_code: str, arrival_code: str, passengers: int,
               departure_date: str, return_date: str) -> str:
        url = self._build_url(departure_code, arrival_code, passengers, departure_date, return_date)
        delay = 3
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, headers=self.HEADERS, timeout=15)
                if response.status_code == 200:
                    result = self._parse(response.text)
                    if result:
                        return result
                time.sleep(delay)
                delay = random.randint(1, 5)
            except requests.RequestException:
                time.sleep(delay)
                delay = random.randint(1, 5)

        browser_result = self._search_with_browser(url)
        if browser_result and "unavailable" not in browser_result:
            return browser_result

        if departure_code.upper() == "BER" and arrival_code.upper() == "BCN":
            reason = browser_result or "No live flight data could be parsed."
            return f"{FLIGHTS_BER_BCN}\n\nLive flight request failed: {reason}"

        return "Es gibt keine Fluege."

    def _build_url(self, dep, arr, passengers, dep_date, ret_date) -> str:
        base = f"{self.BASE_URL}/{dep}-{arr}/{dep_date}/{ret_date}"
        if passengers > 1:
            base += f"/{passengers}adults"
        return base + "?ucs=3ccv3e&sort=price_a"

    def _parse(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        current_results = self._parse_current_swoodoo_cards(soup)
        if current_results:
            return current_results

        prices = soup.find_all("div", class_="f8F1-price-text")
        durations = soup.find_all("div", class_="vmXl vmXl-mod-variant-large")
        operators = soup.find_all("div", class_="J0g6-operator-text")
        stops = soup.find_all("span", class_="JWEO-stops-text")
        if not (prices and operators and durations and stops):
            return ""
        results = []
        for i, (price, operator) in enumerate(zip(prices, operators)):
            dur = durations[i * 2: i * 2 + 2]
            stp = stops[i * 2: i * 2 + 2]
            if len(dur) < 2 or len(stp) < 2:
                continue
            results.append(
                f"Option {i+1}: {operator.text.strip()} | Price: {price.text.strip()} | "
                f"Outbound: {dur[0].text.strip()} ({stp[0].text.strip()}) | "
                f"Return: {dur[1].text.strip()} ({stp[1].text.strip()})"
            )
        return "\n".join(results)

    def _parse_current_swoodoo_cards(self, soup: BeautifulSoup) -> str:
        cards = soup.find_all("div", class_="nrc6-mod-pres-default")
        results = []
        for card in cards:
            price = self._text(card.find("div", class_="e2GB-price-text"))
            operator = self._text(card.find("div", class_="J0g6-operator-text"))
            routes = [self._text(item) for item in card.find_all("div", class_="VY2U")]
            details = [
                self._text(item)
                for item in card.find_all("div", class_="vmXl-mod-variant-default")
            ]

            if not (price and operator and len(routes) >= 2):
                continue

            outbound_stop = details[0] if len(details) > 0 else ""
            outbound_duration = details[1] if len(details) > 1 else ""
            return_stop = details[2] if len(details) > 2 else ""
            return_duration = details[-1] if len(details) > 3 else ""

            results.append(
                f"Option {len(results) + 1}: {operator} | Price: {price} | "
                f"Outbound: {routes[0]} ({outbound_stop}, {outbound_duration}) | "
                f"Return: {routes[1]} ({return_stop}, {return_duration})"
            )
            if len(results) >= 5:
                break

        return "\n".join(results)

    def _text(self, element) -> str:
        if not element:
            return ""
        return " ".join(element.get_text(" ", strip=True).split())

    def _search_with_browser(self, url: str) -> str:
        self._configure_windows_event_loop()
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            return (
                "Flight browser search requires Playwright. "
                "Run: pip install -r requirements.txt && python -m playwright install chromium"
            )

        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.HEADERS["User-Agent"],
                    locale="de-DE",
                    extra_http_headers={"Accept-Language": "de-DE,de;q=0.9,en;q=0.8"},
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                self._close_consent_dialog(page)
                page.wait_for_timeout(12000)
                html = page.content()
                browser.close()
            return self._parse(html)
        except Exception as exc:
            return f"Flight browser search unavailable: {type(exc).__name__}: {str(exc).splitlines()[0]}"

    def _close_consent_dialog(self, page) -> None:
        for label in ("Alle ablehnen", "Ablehnen", "Akzeptieren", "Einverstanden"):
            try:
                button = page.get_by_role("button", name=label)
                if button.count() > 0:
                    button.first.click(timeout=2000)
                    page.wait_for_timeout(1000)
                    return
            except Exception:
                continue

    def _configure_windows_event_loop(self) -> None:
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
