import streamlit as st
from groq import Groq
from datetime import datetime
import html
import json
import streamlit.components.v1 as components

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="XO AI — Free Version",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------------------------------------
# GROQ CLIENT
# -----------------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------------------------------------
# SYSTEM PROMPT
# -----------------------------------------------------------
SYSTEM_PROMPT = """
You are XO AI, a professional, calm, intelligent assistant created by Nexo.corp.

Rules:
- Speak clearly, maturely, respectfully.
- Strong in academics, maths, coding, business, psychology, and productivity.
- Emotion-aware: respond with empathy if user is sad or stressed.
- Clean, short paragraphs + bullet points when helpful.
- No cringe. No childish tone.
- If unsure, admit uncertainty politely.
"""

# -----------------------------------------------------------
# SESSION
# -----------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello, I’m XO AI. How can I help you today?",
            "time": datetime.now().strftime("%I:%M %p"),
        }
    ]


def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "time": datetime.now().strftime("%I:%M %p"),
    })


# -----------------------------------------------------------
# STYLE — SUPER CLEAN
# -----------------------------------------------------------
st.markdown("""
<style>
body, .stApp {
    background: #111215;
    color: #ffffff;
    font-family: system-ui, sans-serif;
}

.block-container {
    max-width: 900px;
    padding-top: 1rem;
}

header, #MainMenu, footer {visibility: hidden;}

/* Title */
.title {
    font-size: 1.6rem;
    font-weight: 600;
}

/* Chat Panel */
.chat-window {
    background: #15171a;
    border: 1px solid #2d2f33;
    padding: 16px;
    border-radius: 14px;
    max-height: calc(100vh - 260px);
    overflow-y: auto;
    margin-top
