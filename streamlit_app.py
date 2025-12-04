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
    margin-top: 1rem;
}

/* Message bubbles */
.msg-row {
    display: flex;
    margin-bottom: 12px;
}

.msg-row.user { justify-content: flex-end; }
.msg-row.assistant { justify-content: flex-start; }

.bubble {
    max-width: 78%;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 0.95rem;
    line-height: 1.4;
}

.bubble.assistant {
    background: #000000;
    border: 1px solid #303238;
}

.bubble.user {
    background: #1c1f24;
    border: 1px solid #3a3d42;
}

/* Timestamp */
.time {
    font-size: 0.7rem;
    color: #9ca3af;
    margin-top: 3px;
    text-align: right;
}

/* Copy button */
.copy-row {
    display: flex;
    justify-content: flex-end;
    margin-top: 2px;
}

.copy-row .stButton button {
    font-size: 0.7rem;
    padding: 2px 10px;
    background: #1c1f24;
    color: #cccccc;
    border-radius: 999px;
    border: 1px solid #333336;
}
.copy-row .stButton button:hover {
    background: #2a2d32;
    color: white;
}

/* Input bar */
.input-box {
    background: #15171a;
    border: 1px solid #2b2e33;
    border-radius: 999px;
    padding: 6px 14px;
    margin-top: 1rem;
}

.stButton>button {
    background: #6366f1;
    border-radius: 999px;
    border: none;
    color: white;
    padding: 6px 20px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown("<div class='title'>XO AI (Free)</div>", unsafe_allow_html=True)
with col2:
    if st.button("New chat"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "New chat started. What can I do for you?",
            "time": datetime.now().strftime("%I:%M %p"),
        }]
        st.rerun()

st.write("---")

# -----------------------------------------------------------
# MODEL SELECT
# -----------------------------------------------------------
model_choice = st.selectbox("Choose free Groq model:", [
    "LLaMA-3.1-8B (fast & smart)",
    "Mixtral-8x7B (strong reasoning)",
    "Gemma-2-9B (clean tone)"
])

MODEL_MAP = {
    "LLaMA-3.1-8B (fast & smart)": "llama-3.1-8b-instant",
    "Mixtral-8x7B (strong reasoning)": "mixtral-8x7b-32768",
    "Gemma-2-9B (clean tone)": "gemma2-9b-it",
}

MODEL_NAME = MODEL_MAP[model_choice]

# -----------------------------------------------------------
# CHAT WINDOW
# -----------------------------------------------------------
st.markdown("<div class='chat-window'>", unsafe_allow_html=True)

def safe_html(text):
    return html.escape(text).replace("\n", "<br>")

for i, msg in enumerate(st.session_state.messages):
    role = msg["role"]
    cls = "user" if role == "user" else "assistant"
    text = safe_html(msg["content"])
    time_str = msg["time"]

    st.markdown(
        f"""
        <div class="msg-row {cls}">
            <div class="bubble {cls}">
                {text}
                <div class="time">{time_str}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Copy button only for assistant
    if role == "assistant":
        st.markdown("<div class='copy-row'>", unsafe_allow_html=True)
        if st.button("📋 Copy", key=f"copy_{i}"):
            components.html(
                f"""
                <script>
                    navigator.clipboard.writeText({json.dumps(msg["content"])});
                </script>
                """,
                height=0, width=0
            )
            st.toast("Copied!")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# INPUT AREA
# -----------------------------------------------------------
st.markdown("<div class='input-box'>", unsafe_allow_html=True)
with st.form("input", clear_on_submit=True):
    c1, c2 = st.columns([0.85, 0.15])
    with c1:
        user_text = st.text_input("", placeholder="Ask XO AI anything...")
    with c2:
        send = st.form_submit_button("Send")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# HANDLE SEND
# -----------------------------------------------------------
if send and user_text.strip():
    text = user_text.strip()
    add_message("user", text)

    with st.spinner("XO is thinking..."):
        reply = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        ).choices[0].message.content

    add_message("assistant", reply)
    st.rerun()
