import os
import sys
from pathlib import Path

import openai
from dotenv import load_dotenv, set_key

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
ENV_FILE = PROJECT_ROOT / ".env"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from services.bluesky_service import BlueskyService

load_dotenv(ENV_FILE)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INSTRUCTIONS = """
You are Smart Journey AI – a personal AI travel planner. Your mission is to help
users plan unforgettable trips that match their lifestyle, preferences, schedule, and budget.

## Planning Process

### Step 1 – Orient Yourself
Always call get_current_date first. Search the user profile and Bluesky/social posts
(file_search) to learn their preferences, interests, travel style, and activity patterns.
Call get_user_memory to include saved long-term preferences such as diet, hotel style,
budget, mobility needs, and interests. If the user explicitly says "remember", "save",
or "merke dir", call save_user_memory.
If the user gives feedback about a recommendation, for example "too expensive",
"I prefer central hotels", or "remember that I am vegetarian", call learn_from_feedback.

### Step 2 – Find Travel Window
- No dates given? Call get_calendar_events for the next 3–6 months.
  Find conflict-free windows that use public holidays efficiently.
- If the user asks for the best travel period or only gives a broad month/range,
  call find_best_travel_windows and explain why the selected windows are useful.
- Dates given? Check for calendar conflicts.

### Step 3 – Destination & Weather
Propose a destination. Call get_weather_forecast to verify conditions.
Poor weather? Suggest an alternative.

### Step 4 – Search Options
Run both searches and present 3 options each:
✈️ Flights (search_flights) – airline, price, duration, stops
🏨 Hotels (search_hotels) – name, price/night, rating, distance
Never tell the user to search flights or hotels by themselves when these tools are available.
If a tool returns results, include concrete flight and hotel options in the answer.
If a tool fails, explain that the system tried the source and show a short fallback plan.

### Step 5 – Build Itinerary
Draft a day-by-day plan with a packing list. If Bluesky/social posts are available,
explain briefly which interests influenced the recommendation.
Call estimate_trip_budget and calculate_risk_score when enough trip details are available.
Call create_packing_list when the user asks for preparation, packing, or a complete agency-style plan.

### Step 6 – Ask User to Choose
> "Please choose your preferred flight (1/2/3) and hotel (1/2/3)."

### Step 7 – Finalise
Once confirmed:
0. Call run_quality_check for the selected plan.
0. Call save_trip_plan to store the trip as a travel file for later updates.
1. Call send_travel_email with complete details and .ics attachment.
2. Call publish_travel_post (≤300 chars, travel emojis, #SmartJourneyAI).

### Step 8 – Travel Agency Follow-up
If the user asks to update, monitor, or re-check a saved trip, call get_saved_trips
and check_trip_updates. Explain what changed and suggest practical adjustments,
for example indoor activities during extreme heat or switching hotels if prices changed.
If check_trip_updates returns an action_plan or next_action, summarize it clearly.

## Guidelines
- Always use get_current_date before planning.
- For trip planning requests with destination and dates, always call get_weather_forecast,
  search_flights, and search_hotels before writing the final recommendation.
- Use Bluesky/social posts from file_search when the user asks for personalization.
- Use saved memory for personalization even if the user does not repeat preferences.
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
    {"type": "function", "function": {"name": "get_user_memory", "description": "Load saved long-term user preferences for personalization.", "strict": True, "parameters": {"type": "object", "properties": {}, "additionalProperties": False}}},
    {"type": "function", "function": {"name": "save_user_memory", "description": "Save long-term user preferences such as diet, budget, hotel style, interests, or mobility needs.", "parameters": {"type": "object", "properties": {"preferences": {"type": "object", "additionalProperties": True}}, "required": ["preferences"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "learn_from_feedback", "description": "Learn travel preferences from natural user feedback after a recommendation.", "strict": True, "parameters": {"type": "object", "properties": {"feedback": {"type": "string"}}, "required": ["feedback"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "get_saved_trips", "description": "Load saved travel files for later updates or monitoring.", "strict": True, "parameters": {"type": "object", "properties": {}, "additionalProperties": False}}},
    {"type": "function", "function": {"name": "save_trip_plan", "description": "Save a confirmed or planned trip as a travel file.", "parameters": {"type": "object", "properties": {"trip": {"type": "object", "additionalProperties": True}}, "required": ["trip"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "update_trip_weather", "description": "Update the weather summary of a saved trip and report whether something changed.", "strict": True, "parameters": {"type": "object", "properties": {"trip_id": {"type": "string"}, "weather_summary": {"type": "string"}}, "required": ["trip_id", "weather_summary"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "run_quality_check", "description": "Evaluate whether a trip plan contains destination, dates, weather, flights, hotels, and personalization.", "parameters": {"type": "object", "properties": {"plan": {"type": "object", "additionalProperties": True}}, "required": ["plan"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "check_trip_updates", "description": "Re-check a saved trip and detect changed weather, flight, or hotel data.", "strict": True, "parameters": {"type": "object", "properties": {"trip_id": {"type": "string"}}, "required": ["trip_id"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "estimate_trip_budget", "description": "Estimate total trip budget from saved or selected flight, hotel, and daily-cost data.", "parameters": {"type": "object", "properties": {"trip": {"type": "object", "additionalProperties": True}}, "required": ["trip"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "create_packing_list", "description": "Create a packing list based on trip weather and saved user preferences.", "parameters": {"type": "object", "properties": {"trip": {"type": "object", "additionalProperties": True}, "preferences": {"type": "object", "additionalProperties": True}}, "required": ["trip"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "calculate_risk_score", "description": "Calculate travel risk based on data completeness, alerts, and reliability.", "parameters": {"type": "object", "properties": {"trip": {"type": "object", "additionalProperties": True}}, "required": ["trip"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "find_best_travel_windows", "description": "Find the best free travel windows using Google Calendar, public holidays, weekends, and weather.", "parameters": {"type": "object", "properties": {"destination": {"type": "string"}, "earliest_date": {"type": "string"}, "latest_date": {"type": "string"}, "duration_days": {"type": "number"}, "max_results": {"type": "number"}}, "required": ["destination", "earliest_date", "latest_date", "duration_days"], "additionalProperties": False}}},
]


def setup_assistant():
    print("=" * 50)
    print("  Smart Journey AI – Setup")
    print("=" * 50)

    file_ids = []

    print("\n[1/4] Uploading user profile if available...")
    profile_path = DATA_DIR / "user_profile.pdf"
    if profile_path.exists():
        with profile_path.open("rb") as file:
            profile_file = client.files.create(file=file, purpose="assistants")
        file_ids.append(profile_file.id)
        print(f"      {profile_file.id}")
    else:
        print("      skipped: data/user_profile.pdf not found")

    print("[2/4] Fetching Bluesky posts if credentials are available...")
    if os.getenv("BLUESKY_USERNAME") and os.getenv("BLUESKY_PASSWORD"):
        BlueskyService().fetch_recent_posts(limit=25)
        print("      Bluesky posts fetched")
    else:
        print("      skipped: Bluesky credentials missing")

    print("[3/4] Uploading social posts if available...")
    posts_path = DATA_DIR / "social_posts.json"
    if posts_path.exists():
        with posts_path.open("rb") as file:
            posts_file = client.files.create(file=file, purpose="assistants")
        file_ids.append(posts_file.id)
        print(f"      {posts_file.id}")
    else:
        print("      skipped: data/social_posts.json not found")

    print("[4/4] Creating assistant and thread...")
    vector_store_id = None
    if file_ids:
        vector_store = client.beta.vector_stores.create(name="Smart Journey AI User Context")
        client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store.id,
            file_ids=file_ids,
        )
        vector_store_id = vector_store.id

    assistant_kwargs = {
        "name": "Smart Journey AI",
        "model": "gpt-4o-mini",
        "instructions": INSTRUCTIONS,
        "tools": TOOLS,
    }
    if vector_store_id:
        assistant_kwargs["tool_resources"] = {
            "file_search": {
                "vector_store_ids": [vector_store_id],
            }
        }

    assistant = client.beta.assistants.create(**assistant_kwargs)
    thread = client.beta.threads.create()

    set_key(str(ENV_FILE), "ASSISTANT_ID", assistant.id)
    set_key(str(ENV_FILE), "THREAD_ID", thread.id)

    print("\n" + "=" * 50)
    print("  Assistant setup completed. .env was updated:")
    print("=" * 50)
    print(f"  ASSISTANT_ID={assistant.id}")
    print(f"  THREAD_ID={thread.id}")
    print("=" * 50)
    return assistant.id, thread.id


if __name__ == "__main__":
    setup_assistant()
