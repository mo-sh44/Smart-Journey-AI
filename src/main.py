import asyncio
import re
import sys
from datetime import datetime, timedelta

import streamlit as st
from dotenv import load_dotenv
from core.demo_mode import create_demo_travel_plan
from core.openai_handler import OpenAIHandler
from services.memory_service import MemoryService
from services.monitoring_service import MonitoringService
from services.travel_agency_service import TravelAgencyService
from services.travel_window_service import TravelWindowService

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv(override=True)

st.set_page_config(page_title="Smart Journey AI", page_icon="SJ", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.stApp { background-color: #ffffff; color: #172033; }
[data-testid="stSidebar"] { background: #f5f7fb; border-right: 1px solid #dfe5ef; }
.hero { font-size: 2.1rem; font-weight: 700; color: #1f4e79; margin-bottom: 0.2rem; }
.sub { color: #5f6f89; font-size: 1rem; margin-top: 0.2rem; }
.status-card {
    border: 1px solid #dbe4ef;
    border-radius: 8px;
    padding: 0.8rem;
    background: #f8fafc;
    margin-bottom: 0.7rem;
}
.status-card strong { color: #1f4e79; }
.trip-card {
    border: 1px solid #dbe4ef;
    border-radius: 8px;
    padding: 1rem;
    background: #ffffff;
    margin-bottom: 0.85rem;
}
.metric-strip {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin: 0.8rem 0 1rem 0;
}
.metric-tile {
    border: 1px solid #dbe4ef;
    border-radius: 8px;
    padding: 0.8rem;
    background: #f8fbff;
}
.metric-tile span { color: #64748b; font-size: 0.82rem; }
.metric-tile strong { display:block; color:#1f4e79; font-size:1.35rem; margin-top:0.2rem; }
.option-card {
    border: 1px solid #dbe4ef;
    border-radius: 8px;
    padding: 0.75rem 0.85rem;
    background: #ffffff;
    margin-bottom: 0.55rem;
}
.option-card strong { color: #1f4e79; }
.change-card {
    border: 1px solid #dbe4ef;
    border-radius: 8px;
    padding: 0.85rem;
    background: #fff;
    margin: 0.55rem 0;
}
.change-card .label { color:#1f4e79; font-weight:700; }
.context-note {
    border: 1px solid #dbe4ef;
    border-radius: 8px;
    padding: 0.7rem 0.85rem;
    background: #f8fafc;
    color: #475569;
}
.section-box {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.9rem;
    background: #fbfdff;
    margin-bottom: 0.8rem;
}
.alert-box {
    border-left: 4px solid #1f4e79;
    padding: 0.75rem 0.9rem;
    background: #f1f7ff;
    margin: 0.5rem 0 0.8rem 0;
}
.muted { color: #64748b; font-size: 0.9rem; }
.pill {
    display: inline-block;
    border: 1px solid #cbd5e1;
    border-radius: 999px;
    padding: 0.15rem 0.55rem;
    margin: 0.1rem 0.2rem 0.1rem 0;
    background: #f8fafc;
    font-size: 0.82rem;
}
div[data-testid="stButton"] > button {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    color: #172033;
    border-radius: 6px;
    font-size: 0.88rem;
    padding: 0.45rem 0.8rem;
}
div[data-testid="stButton"] > button:hover {
    background: #eef5ff;
    border-color: #1f4e79;
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

memory_service = MemoryService()
monitoring_service = MonitoringService()
agency_service = TravelAgencyService()
travel_window_service = TravelWindowService()
AUTO_CHECK_INTERVAL_MINUTES = 30


def create_demo_trip():
    return memory_service.save_trip(
        {
            "destination": "Barcelona",
            "departure_code": "BER",
            "arrival_code": "BCN",
            "start_date": "2026-07-10",
            "end_date": "2026-07-14",
            "adults": 1,
            "rooms": 1,
            "weather_summary": "2026-07-10: 29.0°C - 33.7°C, Partially cloudy",
            "flight_summary": "Option 1: Lufthansa | Price: 176 EUR | Outbound: 2h 15m (direct) | Return: 2h 20m (direct)",
            "hotel_summary": "Hotel 1: W Barcelona | Preis: 223 EUR/Nacht | Bewertung: 8.9 | Entfernung: 0.8 km",
            "personalization_notes": "Vegan food, culture, cafes, beach, and photography spots.",
            "daily_budget": 60,
            "status": "confirmed",
        }
    )


def trip_label(trip):
    return f"{trip.get('destination', 'Trip')} · {trip.get('start_date', '?')} to {trip.get('end_date', '?')}"


def trip_internal_context(trip):
    return (
        "Nutze diese intern gespeicherte Reiseakte als Kontext. Zeige dem Nutzer keine Trip ID.\n"
        f"Interne Trip ID: {trip.get('id')}\n"
        f"Ziel: {trip.get('destination')}\n"
        f"Zeitraum: {trip.get('start_date')} bis {trip.get('end_date')}\n"
        f"Flug: {trip.get('flight_summary', 'noch nicht gespeichert')}\n"
        f"Hotel: {trip.get('hotel_summary', 'noch nicht gespeichert')}\n"
        f"Wetter: {trip.get('weather_summary', 'noch nicht gespeichert')}\n"
        f"Personalisierung: {trip.get('personalization_notes', 'noch nicht gespeichert')}\n"
    )


def split_entries(text):
    compact = " ".join((text or "").split())
    if not compact:
        return []
    markers = list(re.finditer(r"(?=(?:Option|Hotel)\s+\d+:|\d{4}-\d{2}-\d{2}:)", compact))
    if len(markers) <= 1:
        return [compact]
    entries = []
    for index, marker in enumerate(markers):
        start = marker.start()
        end = markers[index + 1].start() if index + 1 < len(markers) else len(compact)
        entries.append(compact[start:end].strip())
    return entries


def render_option_list(title, text):
    st.markdown(f"**{title}**")
    entries = split_entries(text)
    if not entries:
        st.caption(f"No {title.lower()} saved.")
        return
    for entry in entries:
        parts = [part.strip() for part in entry.split("|")]
        headline = parts[0]
        details = " · ".join(parts[1:]) if len(parts) > 1 else ""
        detail_html = f"<br><span class='muted'>{details}</span>" if details else ""
        st.markdown(
            f"<div class='option-card'><strong>{headline}</strong>"
            f"{detail_html}</div>",
            unsafe_allow_html=True,
        )


def render_weather_list(text):
    st.markdown("**Weather**")
    entries = split_entries(text)
    if not entries:
        st.caption("No weather saved.")
        return
    for entry in entries:
        st.markdown(f"<span class='pill'>{entry}</span>", unsafe_allow_html=True)


def render_alert_summary(alert):
    if not alert:
        st.info("No monitoring result available yet.")
        return
    message = alert.get("message", "No update message.")
    recommendation = alert.get("recommendation", "No recommendation available.")
    checked_at = alert.get("checked_at", "unknown")
    changes = alert.get("changes", [])

    if alert.get("changes_detected"):
        st.warning(message)
    else:
        st.success(message)
    st.markdown(
        f"<div class='alert-box'><strong>Last checked:</strong> {checked_at}<br>"
        f"<strong>Recommendation:</strong> {recommendation}</div>",
        unsafe_allow_html=True,
    )
    if changes:
        st.markdown("**What changed**")
        for change in changes:
            st.markdown(
                f"<div class='change-card'>"
                f"<div class='label'>{change.get('type', 'Update').title()}</div>"
                f"<strong>{change.get('summary', 'Data changed.')}</strong><br>"
                f"<span class='muted'>Before:</span> {change.get('before', 'Not available')}<br>"
                f"<span class='muted'>After:</span> {change.get('after', 'Not available')}<br>"
                f"<span class='muted'>Impact:</span> {change.get('impact', 'Review recommended.')}"
                f"</div>",
                unsafe_allow_html=True,
            )
    action_plan = alert.get("action_plan", [])
    if action_plan:
        st.markdown("**Suggested action plan**")
        for action in action_plan:
            st.write(f"- {action}")
    if alert.get("next_action"):
        st.info(f"Next action: {alert['next_action']}")


def render_trip_card(trip, compact=False, show_monitoring=False, show_packing=True):
    title = f"{trip.get('destination', 'Unknown trip')} · {trip.get('start_date', '?')} to {trip.get('end_date', '?')}"
    st.markdown(
        f"<div class='trip-card'><strong>{title}</strong><br>"
        f"<span class='muted'>Status: {trip.get('status', 'planned')} · Last check: {trip.get('last_checked_at', 'not checked yet')}</span></div>",
        unsafe_allow_html=True,
    )
    if compact:
        return
    budget = trip.get("budget") or agency_service.estimate_budget(trip)
    risk = trip.get("risk") or agency_service.risk_score(trip)
    st.markdown(
        f"<div class='metric-strip'>"
        f"<div class='metric-tile'><span>Estimated budget</span><strong>{budget.get('estimated_total', 0)} {budget.get('currency', 'EUR')}</strong></div>"
        f"<div class='metric-tile'><span>Risk level</span><strong>{risk.get('level', 'low').title()}</strong></div>"
        f"<div class='metric-tile'><span>Monitoring updates</span><strong>{len(trip.get('alerts', []))}</strong></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    render_option_list("Flights", trip.get("flight_summary", ""))
    render_option_list("Hotels", trip.get("hotel_summary", ""))
    render_weather_list(trip.get("weather_summary", ""))
    st.markdown("**Personalization**")
    notes = trip.get("personalization_notes", "No personalization notes saved.")
    st.markdown(f"<div class='option-card'>{notes}</div>", unsafe_allow_html=True)

    if show_packing:
        with st.expander("Packing list and risk details"):
            preferences = memory_service.get_user_memory().get("preferences", {})
            for item in agency_service.create_packing_list(trip, preferences):
                st.write(f"- {item}")
            st.markdown("**Risk reasons**")
            for reason in risk.get("reasons", []):
                st.write(f"- {reason}")
    alerts = trip.get("alerts", [])
    if show_monitoring and alerts:
        render_alert_summary(alerts[-1])


def is_monitoring_due(trip):
    last_checked = trip.get("last_checked_at")
    if not last_checked:
        return True
    try:
        checked_at = datetime.fromisoformat(last_checked)
    except ValueError:
        return True
    return datetime.now() - checked_at >= timedelta(minutes=AUTO_CHECK_INTERVAL_MINUTES)

with st.sidebar:
    st.markdown("<h2 style='color:#1f4e79;'>Smart Journey AI</h2><p style='color:#5f6f89;font-size:0.9rem;'>AI-powered travel planning</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### Demo profile")
    memory = memory_service.get_user_memory()
    preferences = memory.get("preferences", {})
    with st.expander("Saved preferences", expanded=True):
        diet = st.text_input("Diet", value=preferences.get("diet", ""), placeholder="vegan, vegetarian, halal...")
        hotel_style = st.text_input("Hotel style", value=preferences.get("hotel_style", ""), placeholder="central, boutique, budget...")
        budget = st.text_input("Budget", value=preferences.get("budget", ""), placeholder="low, medium, premium...")
        interests_text = st.text_input(
            "Interests",
            value=", ".join(preferences.get("interests", [])) if isinstance(preferences.get("interests"), list) else str(preferences.get("interests", "")),
            placeholder="culture, cafes, photography",
        )
        if st.button("Save profile", use_container_width=True):
            memory_service.update_user_memory(
                {
                    "diet": diet,
                    "hotel_style": hotel_style,
                    "budget": budget,
                    "interests": [item.strip() for item in interests_text.split(",") if item.strip()],
                }
            )
            st.success("Profile saved.")
    saved_trips = memory_service.get_saved_trips()
    with st.expander(f"Travel files ({len(saved_trips)})", expanded=False):
        if st.button("Create demo travel file", use_container_width=True):
            create_demo_trip()
            st.rerun()
        if not saved_trips:
            st.caption("No saved trips yet.")
        for trip in saved_trips[-3:]:
            st.markdown(
                f"<div class='status-card'><strong>{trip.get('destination', 'Trip')}</strong><br>"
                f"{trip.get('start_date', '?')} to {trip.get('end_date', '?')}<br>"
                f"<span class='muted'>{trip.get('status', 'planned')}</span></div>",
                unsafe_allow_html=True,
            )
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        "1. 💬 Tell me where to go\n"
        "2. 👤 I remember your preferences\n"
        "3. 📅 I check your calendar\n"
        "4. ☀️ I verify the weather\n"
        "5. ✈️ I find flights and hotels\n"
        "6. 📧 You get a confirmation email\n"
        "7. 🌐 Trip can be shared on BlueSky"
    )
    st.divider()
    mode = st.radio(
        "Mode",
        ["OpenAI Assistant", "Demo mode"],
        help="OpenAI Assistant uses tools. Demo mode is a deterministic fallback.",
    )
    auto_monitoring = st.checkbox(
        "Auto-check saved trips every 30 min",
        value=True,
        help="Works while the app is open. For the demo, use 'Check updates now'.",
    )
    st.divider()
    st.markdown("### Quick Start")
    for prompt in [
        "Merke dir: Ich bin vegan, mag zentrale Hotels und interessiere mich fuer Kultur, Cafes und Fotospots.",
        "Ich möchte im August 2026 für 5 Tage nach Barcelona. Finde den besten Reisezeitraum.",
        "Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026.",
        "Aktualisiere meine gespeicherte Barcelona-Reise und pruefe, ob sich das Wetter geaendert hat.",
        "Das Hotel ist mir zu teuer. Merke dir bitte, dass ich guenstige zentrale Hotels bevorzuge.",
        "City break in Europe this summer",
        "Plan a beach holiday next month",
        "Winter trip to the Alps",
    ]:
        if st.button(prompt, use_container_width=True, key=f"q_{prompt[:15]}"):
            st.session_state.pending = prompt
    st.divider()
    st.caption("HTW Berlin project prototype")

st.markdown("<h1 class='hero'>Smart Journey AI</h1><p class='sub'>From chatbot to personal travel agency: memory, tools, travel files, and live updates.</p>", unsafe_allow_html=True)
st.divider()

tab_chat, tab_trips, tab_windows, tab_alerts = st.tabs(["Assistant", "Travel files", "Best travel window", "Monitoring"])

if "messages" not in st.session_state:
    st.session_state.messages = []
if mode == "OpenAI Assistant" and "handler" not in st.session_state:
    st.session_state.handler = OpenAIHandler()

with tab_trips:
    st.subheader("Travel files")
    st.caption("This is the saved customer travel file: current plan, selected options, budget, packing list, and personalization.")
    trips = memory_service.get_saved_trips()
    if st.button("Create Barcelona demo file", key="create_demo_main"):
        create_demo_trip()
        st.rerun()
    if not trips:
        st.info("No travel files saved yet. Create a demo file or confirm a trip through the assistant.")
    else:
        trip_options = [
            (f"{index + 1}. {trip_label(trip)}", trip["id"])
            for index, trip in enumerate(reversed(trips))
        ]
        selected_trip_label = st.selectbox("Open travel file", [label for label, _trip_id in trip_options], key="travel_file_select")
        selected_trip_id = dict(trip_options)[selected_trip_label]
        selected_trip = memory_service.get_trip(selected_trip_id)
        if selected_trip:
            top_cols = st.columns([1, 1, 1])
            if top_cols[0].button("Chat about this trip", use_container_width=True):
                st.session_state.active_trip_context = trip_internal_context(selected_trip)
                st.session_state.pending = f"Ich habe eine Frage zu meiner {selected_trip.get('destination', 'Reise')}-Reise."
                st.rerun()
            if top_cols[1].button("Check this trip now", use_container_width=True):
                with st.spinner("Refreshing this travel file..."):
                    result = monitoring_service.check_trip_updates(selected_trip["id"])
                render_alert_summary(result.get("alert", {}))
                st.rerun()
            if top_cols[2].button("Duplicate demo file", use_container_width=True):
                create_demo_trip()
                st.rerun()
            render_trip_card(selected_trip)

with tab_alerts:
    st.subheader("Monitoring and updates")
    st.caption("This is the active monitoring view: it compares the saved travel file with fresh data and recommends the next action.")
    trips = memory_service.get_saved_trips()
    if not trips:
        st.info("No trip available for monitoring yet.")
    else:
        if auto_monitoring:
            st.markdown(
                "<meta http-equiv='refresh' content='1800'>",
                unsafe_allow_html=True,
            )
        option_pairs = [
            (f"{index + 1}. {trip.get('destination', 'Trip')} ({trip.get('start_date', '?')})", trip["id"])
            for index, trip in enumerate(reversed(trips))
        ]
        options = dict(option_pairs)
        selected_label = st.selectbox("Select trip", list(options.keys()))
        selected_trip = memory_service.get_trip(options[selected_label])
        if auto_monitoring and selected_trip and is_monitoring_due(selected_trip):
            with st.spinner("Automatic monitoring check is running..."):
                auto_result = monitoring_service.check_trip_updates(options[selected_label])
            auto_alert = auto_result.get("alert", {})
            if auto_alert.get("changes_detected"):
                st.warning(f"Automatic update: {auto_alert.get('message')}")
            else:
                st.info(f"Automatic update: {auto_alert.get('message')}")
        if st.button("Check updates now", type="primary"):
            with st.spinner("Checking weather, flight, and hotel updates..."):
                result = monitoring_service.check_trip_updates(options[selected_label])
            alert = result.get("alert", {})
            render_alert_summary(alert)
        selected_trip = memory_service.get_trip(options[selected_label])
        if selected_trip:
            if st.button("Open assistant chat for this trip", use_container_width=True):
                st.session_state.active_trip_context = trip_internal_context(selected_trip)
                st.session_state.pending = f"Ich habe eine Frage zu meiner {selected_trip.get('destination', 'Reise')}-Reise."
                st.rerun()
            latest_alerts = selected_trip.get("alerts", [])
            if latest_alerts:
                render_alert_summary(latest_alerts[-1])
            with st.expander("Open refreshed travel file"):
                render_trip_card(selected_trip, show_packing=False)

with tab_windows:
    st.subheader("Best travel window")
    st.caption("Use this when the user does not know exact dates. The agent combines calendar availability, vacation/free entries, public holidays, weekends, and weather.")
    st.markdown(
        "<div class='context-note'><strong>How to demo it:</strong> Add a Google Calendar entry named "
        "<strong>Urlaub</strong> or <strong>frei</strong> in the search period. Smart Journey AI treats those days as preferred travel time, "
        "while normal appointments are treated as blocked.</div>",
        unsafe_allow_html=True,
    )
    window_cols = st.columns([1.2, 1, 1, 0.8])
    destination = window_cols[0].text_input("Destination", value="Barcelona")
    earliest_date = window_cols[1].date_input("Earliest date", value=datetime(2026, 8, 1))
    latest_date = window_cols[2].date_input("Latest date", value=datetime(2026, 8, 31))
    duration_days = window_cols[3].number_input("Days", min_value=2, max_value=21, value=5)
    if st.button("Find best travel windows", type="primary", use_container_width=True):
        with st.spinner("Checking calendar, holidays, weekends, and weather..."):
            result = travel_window_service.find_best_windows(
                destination=destination,
                earliest_date=earliest_date.isoformat(),
                latest_date=latest_date.isoformat(),
                duration_days=int(duration_days),
            )
        if "error" in result:
            st.error(result.get("message", result["error"]))
        else:
            st.success(result["message"])
            summary = result.get("calendar_summary", {})
            if summary.get("warning"):
                st.warning(summary["warning"])
            metric_cols = st.columns(3)
            metric_cols[0].metric("Busy days", summary.get("busy_days", 0))
            metric_cols[1].metric("Preferred days", summary.get("preferred_days", 0))
            metric_cols[2].metric("Holiday days", summary.get("holiday_days", 0))
            for index, window in enumerate(result.get("best_windows", []), start=1):
                with st.container():
                    st.markdown(
                        f"<div class='trip-card'><strong>Option {index}: {window['start_date']} to {window['end_date']}</strong><br>"
                        f"<span class='muted'>Score: {window['score']} · Preferred days: {window.get('preferred_days', 0)} · Weekend days: {window['weekend_days']} · Holidays: {window['holidays_inside']}</span></div>",
                        unsafe_allow_html=True,
                    )
                    st.write(window.get("reason", ""))
                    st.write(window.get("weather_summary", ""))
                    st.info(window.get("recommendation", ""))

    st.divider()
    st.subheader("Feedback learning")
    feedback_text = st.text_area(
        "Tell Smart Journey AI what should be remembered",
        placeholder="Example: Das Hotel ist mir zu teuer. Ich bevorzuge vegetarische Restaurants und zentrale Hotels.",
    )
    if st.button("Learn from feedback", use_container_width=True):
        result = memory_service.learn_from_feedback(feedback_text)
        st.success(result["message"])
        learned = result.get("learned", [])
        if learned:
            st.markdown("**Learned preferences**")
            for item in learned:
                st.write(f"- {item}")

with tab_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def process(user_input: str):
    visible_input = user_input
    assistant_input = user_input
    if st.session_state.get("active_trip_context"):
        assistant_input = f"{st.session_state.active_trip_context}\nNutzerfrage: {user_input}"

    st.session_state.messages.append({"role": "user", "content": visible_input})
    with st.chat_message("user"):
        st.markdown(visible_input)
    if st.session_state.get("active_trip_context"):
        st.markdown(
            "<div class='context-note'>Active travel file is attached internally. The user does not need to enter a Trip ID.</div>",
            unsafe_allow_html=True,
        )
    if mode == "Demo mode":
        with st.spinner("Checking live weather data..."):
            response = create_demo_travel_plan(assistant_input)
    else:
        try:
            with st.spinner("Planning your journey..."):
                response = st.session_state.handler.send_message(assistant_input)
        except Exception as error:
            response = f"Smart Journey AI could not finish the request: {error}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)


with tab_chat:
    if "pending" in st.session_state:
        process(st.session_state.pop("pending"))
        st.rerun()

    if user_input := st.chat_input("Where would you like to travel?"):
        process(user_input)
