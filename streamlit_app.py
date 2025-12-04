import streamlit as st
from groq import Groq
from datetime import datetime
import html
import json
import streamlit.components.v1 as components

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="XO AI — Free Version",
    page_icon="🤖",
    layout="wide",
)

# -----------------------------
# GROQ CLIENT (FREE MODELS)
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = """
You are XO AI, an advanced professional assistant created by Nexo.corp.

Qualities:
- Mature, calm, respectful.
- Very strong at: academics, maths, coding, tech, business, psychology, productivity, and daily life.
- Emotion-aware: if the user is upset or stressed, respond with empathy first.
- Give clear, structured answers with short paragraphs and bullet points when helpful.
- Avoid cringe or childish language.
- Prefer accuracy and honesty over guessing. If you are not fully sure, say so clearly.
- Tone similar to ChatGPT: polite, helpful, and intelligent; adjust slightly to the user’s mood.
"""

# -----------------------------
# SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    # each message: {role, content, time}
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello, I’m XO AI. How can I help you today?",
            "time": datetime.now().strftime("%I:%M %p"),
        }
    ]


def add_message(role: str, content: str):
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%I:%M %p"),
        }
    )


def new_chat():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "New chat started. What can XO do for you?",
            "time": datetime.now().strftime("%I:%M %p"),
        }
    ]


# -----------------------------
# STYLES (minimal, center chat)
# -----------------------------
st.markdown(
    """
<style>
body, .stApp {
    background: #111215;
    color: #f5f5f5;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.block-container {
    max-width: 900px;
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}
header, #MainMenu, footer {visibility: hidden;}

/* Title */
.chat-title {
    font-size: 1.5rem;
    font-weight: 600;
}

/* Model label */
.model-label {
    font-size: 0.9rem;
    margin-bottom: 0.2rem;
}

/* Chat panel */
.chat-panel {
    margin-top: 0.8rem;
    background: #15171a;
    border-radius: 14px;
    border: 1px solid #2b2e33;
    padding: 14px 16px;
    max-height: calc(100vh - 260px);
    overflow-y: auto;
}

/* Message rows */
.msg-row {
    display: flex;
    margin-bottom: 10px;
}
.msg-row.assistant { justify-content: flex-start; }
.msg-row.user { justify-content: flex-end; }

/* Bubbles */
.bubble {
    max-width: 78%;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 0.95rem;
    line-height: 1.4;
    word-wrap: break-word;
}
.bubble.assistant {
    background: #000000;
    border: 1px solid #303238;
    color: #f5f5f5;
}
.bubble.user {
    background: #1c1f24;
    border: 1px solid #34373d;
    color: #ffffff;
}

/* Timestamp */
.msg-time {
    font-size: 0.7rem;
    color: #9ca3af;
    margin-top: 4px;
    text-align: right;
}

/* Copy button row */
.copy-row {
    display: flex;
    justify-content: flex-end;
    margin-top: 3px;
}
.copy-row .stButton>button {
    font-size: 0.7rem;
    padding: 2px 10px;
    background: transparent;
    border-radius: 999px;
    border: 1px solid #333336;
    color: #a1a1a1;
}
.copy-row .stButton>button:hover {
    background: #1f2124;
    color: #ffffff;
}

/* Input area */
.input-card {
    margin-top: 1rem;
    background: #15171a;
    border-radius: 999px;
    border: 1px solid #2b2e33;
    padding: 6px 10px 6px 14px;
}

/* Text input */
div[data-baseweb="input"] {
    background: transparent !important;
    border: none !important;
}
div[data-baseweb="input"] > div {
    background: transparent !important;
    border: none !important;
}
div[data-baseweb="input"] input {
    background: transparent !important;
    color: #f5f5f5 !important;
    font-size: 0.95rem !important;
}

/* Main Send button */
.stButton>button {
    border-radius: 999px;
    border: 1px solid #6366f1;
    background: #6366f1;
    color: #ffffff;
    font-size: 0.9rem;
    padding: 0.3rem 1rem;
    transition: 0.15s;
}
.stButton>button:hover {
    filter: brightness(1.08);
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# HEADER
# -----------------------------
top_left, top_right = st.columns([0.7, 0.3])
with top_left:
    st.markdown('<div class="chat-title">XO AI — CLEAN TEST</div>', unsafe_allow_html=True)
with top_right:
    if st.button("New chat"):
        new_chat()

st.markdown("<hr/>", unsafe_allow_html=True)

# -----------------------------
# MODEL SELECTOR
# -----------------------------
st.markdown('<div class="model-label">Choose free Groq model:</div>', unsafe_allow_html=True)
model_choice = st.selectbox(
    "",
    [
        "LLaMA-3.1-8B (fast & smart)",
        "Mixtral-8x7B (strong reasoning)",
        "Gemma-2-9B (clean tone)",
    ],
    label_visibility="collapsed",
)

MODEL_MAP = {
    "LLaMA-3.1-8B (fast & smart)": "llama-3.1-8b-instant",
    "Mixtral-8x7B (strong reasoning)": "mixtral-8x7b-32768",
    "Gemma-2-9B (clean tone)": "gemma2-9b-it",
}
MODEL_NAME = MODEL_MAP[model_choice]

# -----------------------------
# CHAT PANEL
# -----------------------------
st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

def format_msg(text: str) -> str:
    return html.escape(text).replace("\n", "<br>")

for idx, msg in enumerate(st.session_state.messages):
    role = msg["role"]
    cls = "user" if role == "user" else "assistant"
    safe_text = format_msg(msg["content"])
    time_str = msg.get("time", "")

    # bubble
    st.markdown(
        f"""
        <div class="msg-row {cls}">
            <div class="bubble {cls}">
                {safe_text}
                <div class="msg-time">{time_str}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # copy button for assistant only
    if role == "assistant":
        st.markdown('<div class="copy-row">', unsafe_allow_html=True)
        if st.button("📋 Copy", key=f"copy_{idx}"):
            components.html(
                f"""
                <script>
                navigator.clipboard.writeText({json.dumps(msg["content"])});
                </script>
                """,
                height=0,
                width=0,
            )
            st.toast("Copied!")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# INPUT
# -----------------------------
st.markdown('<div class="input-card">', unsafe_allow_html=True)
with st.form("chat-input", clear_on_submit=True):
    c1, c2 = st.columns([0.85, 0.15])
    with c1:
        user_text = st.text_input(
            "",
            placeholder="Ask XO AI anything...",
            label_visibility="collapsed",
        )
    with c2:
        send = st.form_submit_button("Send")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# HANDLE SEND
# -----------------------------
if send and user_text.strip():
    content = user_text.strip()
    add_message("user", content)

    with st.spinner("XO is thinking..."):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}]
            + st.session_state.messages,
        )
        reply = response.choices[0].message.content

    add_message("assistant", reply)
    st.rerun()
