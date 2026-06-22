import asyncio
import sys

import streamlit as st
from dotenv import load_dotenv
from core.demo_mode import create_demo_travel_plan
from core.openai_handler import OpenAIHandler

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

load_dotenv()

st.set_page_config(page_title="Smart Journey AI", page_icon="SJ", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.stApp { background-color: #ffffff; color: #172033; }
[data-testid="stSidebar"] { background: #f5f7fb; border-right: 1px solid #dfe5ef; }
.hero { font-size: 2.1rem; font-weight: 700; color: #1f4e79; margin-bottom: 0.2rem; }
.sub { color: #5f6f89; font-size: 1rem; margin-top: 0.2rem; }
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

with st.sidebar:
    st.markdown("<h2 style='color:#1f4e79;'>Smart Journey AI</h2><p style='color:#5f6f89;font-size:0.9rem;'>AI-powered travel planning</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### How it works")
    st.markdown(
        "1. 💬 Tell me where to go\n"
        "2. 📅 I check your calendar\n"
        "3. ☀️ I verify the weather\n"
        "4. ✈️ I find flights and hotels\n"
        "5. 📧 You get a confirmation email\n"
        "6. 🌐 Trip can be shared on BlueSky"
    )
    st.divider()
    mode = st.radio(
        "Mode",
        ["OpenAI Assistant", "Demo mode"],
        help="OpenAI Assistant uses tools. Demo mode is a deterministic fallback.",
    )
    st.divider()
    st.markdown("### Quick Start")
    for prompt in [
        "Ich plane eine Reise von Berlin nach Barcelona vom 10.07.2026 bis 14.07.2026.",
        "City break in Europe this summer",
        "Plan a beach holiday next month",
        "Winter trip to the Alps",
    ]:
        if st.button(prompt, use_container_width=True, key=f"q_{prompt[:15]}"):
            st.session_state.pending = prompt
    st.divider()
    st.caption("HTW Berlin project prototype")

st.markdown("<h1 class='hero'>Smart Journey AI</h1><p class='sub'>Travel planning prototype with live weather data and agent-ready tools.</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
if mode == "OpenAI Assistant" and "handler" not in st.session_state:
    st.session_state.handler = OpenAIHandler()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def process(user_input: str):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    if mode == "Demo mode":
        with st.spinner("Checking live weather data..."):
            response = create_demo_travel_plan(user_input)
    else:
        try:
            with st.spinner("Planning your journey..."):
                response = st.session_state.handler.send_message(user_input)
        except Exception as error:
            response = f"Smart Journey AI could not finish the request: {error}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)


if "pending" in st.session_state:
    process(st.session_state.pop("pending"))
    st.rerun()

if user_input := st.chat_input("Where would you like to travel?"):
    process(user_input)
