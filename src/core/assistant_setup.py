import os
import openai
from dotenv import load_dotenv
from services.bluesky_service import BlueskyService

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INSTRUCTIONS = """
You are Smart Journey AI – a personal AI travel planner. Your mission is to help
users plan unforgettable trips that match their lifestyle, preferences, schedule, and budget.

## Planning Process

### Step 1 – Orient Yourself
Always call get_current_date first. Search the user profile (file_search) to learn their preferences.

### Step 2 – Find Travel Window
- No dates given? Call get_calendar_events for the next 3–6 months.
  Find conflict-free windows that use public holidays efficiently.
- Dates given? Check for calendar conflicts.

### Step 3 – Destination & Weather
Propose a destination. Call get_weather_forecast to verify conditions.
Poor weather? Suggest an alternative.

### Step 4 – Search Options
Run both searches and present 3 options each:
✈️ Flights (search_flights) – airline, price, duration, stops
🏨 Hotels (search_hotels) – name, price/night, rating, distance

### Step 5 – Build Itinerary
Draft a day-by-day plan with a packing list.

### Step 6 – Ask User to Choose
> "Please choose your preferred flight (1/2/3) and hotel (1/2/3)."

### Step 7 – Finalise
Once confirmed:
1. Call send_travel_email with complete details and .ics attachment.
2. Call publish_travel_post (≤300 chars, travel emojis, #SmartJourneyAI).

## Guidelines
- Always use get_current_date before planning.
- Keep replies structured with headings and bullets.
- If a service fails, inform the user politely and suggest alternatives.
"""

TOOLS = [
    {"type": "file_search"},
    {"type": "code_interpreter"},
    {"type": "function", "function": {"name": "get_current_date", "description": "Get today's date.", "strict": True, "parameters": {"type": "object", "properties": {}, "additionalProperties": False}}},
    {"type": "function", "function": {"name": "get_weather_forecast", "description": "Get weather forecast for a location and date range.", "strict": True, "parameters": {"type": "object", "properties": {"location": {"type": "string"}, "start_date": {"type": "string"}, "end_date": {"type": "string"}}, "required": ["location", "start_date", "end_date"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "search_flights", "description": "Search for round-trip flights.", "strict": True, "parameters": {"type": "object", "properties": {"departure_code": {"type": "string"}, "arrival_code": {"type": "string"}, "passengers": {"type": "number"}, "departure_date": {"type": "string"}, "return_date": {"type": "string"}}, "required": ["departure_code", "arrival_code", "passengers", "departure_date", "return_date"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "search_hotels", "description": "Search for hotels in a city.", "strict": True, "parameters": {"type": "object", "properties": {"city": {"type": "string"}, "checkin_date": {"type": "string"}, "checkout_date": {"type": "string"}, "adults": {"type": "number"}, "rooms": {"type": "number"}}, "required": ["city", "checkin_date", "checkout_date", "adults", "rooms"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "send_travel_email", "description": "Send a travel confirmation email with .ics attachment.", "strict": True, "parameters": {"type": "object", "properties": {"recipient_email": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}, "calendar_event": {"type": "object", "properties": {"title": {"type": "string"}, "start": {"type": "string"}, "end": {"type": "string"}, "location": {"type": "string"}, "description": {"type": "string"}}, "required": ["title", "start", "end", "location", "description"], "additionalProperties": False}}, "required": ["recipient_email", "subject", "body", "calendar_event"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "publish_travel_post", "description": "Publish a post on Bluesky about the upcoming trip.", "strict": True, "parameters": {"type": "object", "properties": {"post_text": {"type": "string"}}, "required": ["post_text"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "get_calendar_events", "description": "Get user's Google Calendar events and Berlin holidays.", "strict": True, "parameters": {"type": "object", "properties": {"start_date": {"type": "string"}, "end_date": {"type": "string"}}, "required": ["start_date", "end_date"], "additionalProperties": False}}},
]


def setup_assistant():
    print("=" * 50)
    print("  Smart Journey AI – Setup")
    print("=" * 50)

    print("\n[1/4] Uploading user profile...")
    with open("./data/user_profile.pdf", "rb") as f:
        profile_file = client.files.create(file=f, purpose="assistants")
    print(f"      ✓ {profile_file.id}")

    print("[2/4] Fetching Bluesky posts...")
    BlueskyService().fetch_recent_posts(limit=25)

    print("[3/4] Uploading social posts...")
    with open("./data/social_posts.json", "rb") as f:
        posts_file = client.files.create(file=f, purpose="assistants")
    print(f"      ✓ {posts_file.id}")

    print("[4/4] Creating assistant and thread...")
    assistant = client.beta.assistants.create(
        name="Smart Journey AI",
        model="gpt-4-1106-preview",
        instructions=INSTRUCTIONS,
        tools=TOOLS,
    )
    thread = client.beta.threads.create(
        tool_resources={"file_search": {"vector_stores": [{"name": "User Context", "file_ids": [profile_file.id, posts_file.id]}]}}
    )

    vs_id = thread.tool_resources.file_search.vector_store_ids[0]
    client.beta.vector_stores.update(vector_store_id=vs_id, expires_after={"anchor": "last_active_at", "days": 90})

    print("\n" + "=" * 50)
    print("  Add these to your .env file:")
    print("=" * 50)
    print(f"  ASSISTANT_ID={assistant.id}")
    print(f"  THREAD_ID={thread.id}")
    print("=" * 50)
    return assistant.id, thread.id


if __name__ == "__main__":
    setup_assistant()
