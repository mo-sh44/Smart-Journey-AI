# Smart Journey AI – Reiseplanung mit KI

An AI-powered travel planning assistant built for HTW Berlin.

## Features
- 🗓️ Smart date finding via Google Calendar
- ☀️ Weather analysis (Visual Crossing API)
- ✈️ Flight search (Swoodoo)
- 🏨 Hotel search (Booking.com)
- 📧 Email confirmation with .ics attachment
- 🌐 Bluesky social post
- 🤖 Personalised via user profile
- ✅ MVP demo mode with live weather data and no OpenAI API costs

## Structure
```
smart-journey-ai/
├── data/                  ← credentials & user profile (not on GitHub)
├── docs/                  ← API tests, MVP plan, risk documentation
├── src/
│   ├── main.py            ← Streamlit UI
│   ├── core/
│   │   ├── assistant_setup.py
│   │   ├── openai_handler.py
│   │   └── tool_dispatcher.py
│   └── services/
│       ├── weather_service.py
│       ├── flight_service.py
│       ├── hotel_service.py
│       ├── calendar_service.py
│       ├── email_service.py
│       └── bluesky_service.py
├── .env                   ← your secrets (not on GitHub)
├── .env.example
└── requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
copy .env.example .env      # Windows: fill in your local keys
python src/test_weather_api.py
python -m streamlit run src/main.py
```

For the OpenAI Assistant mode, run once:

```bash
python src/core/assistant_setup.py
```

Then copy the generated `ASSISTANT_ID` and `THREAD_ID` into `.env`.

## MVP Demo

For the intermediate presentation, use **Demo mode** in the sidebar. It uses the live Visual Crossing Weather API and creates a travel proposal without OpenAI API costs.

Example prompt:

```text
Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026. Bitte pruefe das Wetter und erstelle einen kurzen Reisevorschlag.
```

## Security

Never commit `.env`, `data/credentials.json`, `data/token.json`, or generated social post data. Use `.env.example` as a template only.

## Team – HTW Berlin
Smart Journey AI Group
