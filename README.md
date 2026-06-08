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

## Structure
```
smart-journey-ai/
├── data/                  ← credentials & user profile (not on GitHub)
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
cp .env.example .env        # fill in your keys
cd src
python -m core.assistant_setup   # run once
streamlit run main.py
```

## Team – HTW Berlin
Smart Journey AI Group
