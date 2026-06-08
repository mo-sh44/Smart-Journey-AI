import streamlit as st
from dotenv import load_dotenv
from core.openai_handler import OpenAIHandler

load_dotenv()

st.set_page_config(page_title="Smart Journey AI", page_icon="✈️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.stApp { background-color: #0f0f1a; color: #e8e8f0; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #12122a, #1a1a3e); border-right: 1px solid #2a2a4a; }
.hero { font-size: 2.2rem; font-weight: 700; background: linear-gradient(135deg, #6c63ff, #48cfad); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.sub { color: #8888aa; font-size: 1rem; margin-top: 0.2rem; }
div[data-testid="stButton"] > button { background: rgba(108,99,255,0.12); border: 1px solid rgba(108,99,255,0.35); color: #c8c4ff; border-radius: 10px; font-size: 0.82rem; padding: 0.45rem 0.8rem; transition: all 0.2s; }
div[data-testid="stButton"] > button:hover { background: rgba(108,99,255,0.28); color: #fff; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#6c63ff;'>✈️ Smart Journey AI</h2><p style='color:#8888aa;font-size:0.85rem;'>Your AI-powered travel planner</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🗺️ How it works")
    st.markdown("1. 💬 Tell me where to go\n2. 📅 I check your calendar\n3. ☀️ I verify the weather\n4. ✈️ I find flights & hotels\n5. 📧 You get a confirmation email\n6. 🌐 Trip shared on Bluesky")
    st.divider()
    st.markdown("### ⚡ Quick Start")
    for prompt in ["Plan a beach holiday next month", "City break in Europe this summer", "Winter trip to the Alps", "Use my next public holiday"]:
        if st.button(prompt, use_container_width=True, key=f"q_{prompt[:15]}"):
            st.session_state.pending = prompt
    st.divider()
    st.caption("🔒 Powered by OpenAI GPT-4 | HTW Berlin")

st.markdown("<h1 class='hero'>Smart Journey AI ✈️</h1><p class='sub'>Tell me your travel dream – I'll handle the rest.</p>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "handler" not in st.session_state:
    st.session_state.handler = OpenAIHandler()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def process(user_input: str):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("✈️ Planning your journey…"):
        response = st.session_state.handler.send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)


if "pending" in st.session_state:
    process(st.session_state.pop("pending"))
    st.rerun()

if user_input := st.chat_input("Where would you like to travel? ✈️"):
    process(user_input)
