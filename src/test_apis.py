import os
import sys

# Ensure UTF-8 output encoding for emojis in Windows console
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add the 'src' directory to python path for easy imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from services.weather_service import WeatherService
from services.bluesky_service import BlueskyService
from services.email_service import EmailService
from services.calendar_service import CalendarService


def test_weather():
    print("\n--- 1. Testing Weather Service (Visual Crossing) ---")
    try:
        weather = WeatherService()
        print("[*] Fetching weather forecast for Berlin...")
        # Get weather for the next 2 days
        import datetime
        today = datetime.date.today().strftime("%Y-%m-%d")
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        result = weather.get_forecast("Berlin", today, tomorrow)
        
        if result:
            print("[+] Weather Service is WORKING! ✅")
            print(f"    Sample Output:\n{result}")
        else:
            print("[-] Weather Service returned no data. ❌ (Check API Key)")
    except Exception as e:
        print(f"[-] Weather Service Failed: {e} ❌")


def test_bluesky():
    print("\n--- 2. Testing Bluesky Service ---")
    try:
        bluesky = BlueskyService()
        if not bluesky.username or not bluesky.password:
            print("[-] Bluesky credentials not set in .env. ❌")
            return
            
        print(f"[*] Logging in as '{bluesky.username}' and fetching recent posts...")
        posts = bluesky.fetch_recent_posts(limit=3)
        print("[+] Bluesky Service is WORKING! ✅")
        print(f"    Fetched {len(posts)} recent posts successfully.")
        for i, post in enumerate(posts, 1):
            text_snippet = post['text'][:50] + "..." if len(post['text']) > 50 else post['text']
            print(f"    Post {i}: {text_snippet}")
    except Exception as e:
        print(f"[-] Bluesky Service Failed: {e} ❌")


def test_email():
    print("\n--- 3. Testing Email Service (SMTP) ---")
    try:
        email_svc = EmailService()
        recipient = "mohamad.shahin@student.htw-berlin.de"
        print(f"[*] Sending test travel email to: {recipient}...")
        
        test_event = {
            "title": "Test Presentation Prep",
            "start": "2026-06-09T10:00:00",
            "end": "2026-06-09T12:00:00",
            "location": "HTW Berlin",
            "description": "Preparing the Smart Journey AI project demo."
        }
        
        result = email_svc.send_travel_confirmation(
            recipient=recipient,
            subject="Smart Journey AI - Test API Connection",
            body="Hello! This email confirms that our SMTP Email API connection is working 100%.",
            event_details=test_event
        )
        
        if "successfully" in result:
            print(f"[+] Email Service is WORKING! ✅ (Check your inbox at {recipient})")
        else:
            print(f"[-] Email Service response: {result} ❌")
    except Exception as e:
        print(f"[-] Email Service Failed: {e} ❌")


def test_calendar():
    print("\n--- 4. Testing Google Calendar API ---")
    try:
        calendar_svc = CalendarService()
        credentials_path = calendar_svc.credentials_path
        
        if not os.path.exists(credentials_path):
            print(f"[-] Google Calendar Credentials missing at: {credentials_path} ❌")
            print("    Please download the 'credentials.json' from Google Cloud Console first.")
            return
            
        print("[*] Authenticating with Google Calendar (This might open a browser window)...")
        import datetime
        today = datetime.date.today().strftime("%Y-%m-%d")
        next_week = (datetime.date.today() + datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        
        events = calendar_svc.get_events(today, next_week)
        if "error" in events:
            print(f"[-] Google Calendar API returned an error: {events['error']} ❌")
        else:
            print("[+] Google Calendar API is WORKING! ✅")
            print(f"    Found {len(events.get('personal', []))} personal events and {len(events.get('holidays', []))} German holidays next week.")
    except Exception as e:
        print(f"[-] Google Calendar API Failed: {e} ❌")


if __name__ == "__main__":
    print("==================================================")
    print("        Smart Journey AI - API Connection Test    ")
    print("==================================================")
    
    test_weather()
    test_bluesky()
    test_email()
    test_calendar()
    
    print("\n==================================================")
