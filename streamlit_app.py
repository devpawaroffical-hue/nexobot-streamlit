import streamlit as st
from groq import Groq

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
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I’m XO AI. How can I help you today?"}
    ]


def new_chat():
    st.session_state.messages = [
        {"role": "assistant", "content": "New chat started. What can XO do for you?"}
    ]


# -----------------------------
# STYLES (custom chat UI)
# -----------------------------
st.markdown(
    """
<style>
/* App background */
body, .stApp {
    background: #111215;
    color: #f5f5f5;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Layout styling */
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

/* Chat panel box */
.chat-panel {
    margin-top: 0.7rem;
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
    margin-bottom: 8px;
}
.msg-row.assistant { justify-content: flex-start; }
.msg-row.user { justify-content: flex-end; }

/* Message bubbles */
.bubble {
    max-width: 78%;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 0.95rem;
    line-height: 1.4;
    word-wrap: break-word;
}

/* Assistant messages: BLACK bubble */
.bubble.assistant {
    background: #000000;
    border: 1px solid #2d2f34;
    color: #f5f5f5;
}

/* User messages: light grey-black */
.bubble.user {
    background: #1c1f24;
    border: 1px solid #34373d;
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

/* Text input inside */
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

/* Send button */
.stButton>button {
    border-radius: 999px;
    border: 1px solid #3b82f6;
    background: #3b82f6;
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
col1, col2 = st.columns([0.75, 0.25])
with col1:
    st.markdown('<div class="chat-title">XO AI (Free)</div>', unsafe_allow_html=True)
with col2:
    if st.button("New chat"):
        new_chat()

st.divider()

# -----------------------------
# MODEL SELECTOR (Groq free)
# -----------------------------
model_choice = st.selectbox(
    "Choose free Groq model:",
    [
        "LLaMA-3.1-8B (fast & smart)",
        "Mixtral-8x7B (strong reasoning)",
        "Gemma-2-9B (clean tone)",
    ],
)

MODEL_MAP = {
    "LLaMA-3.1-8B (fast & smart)": "llama-3.1-8b-instant",
    "Mixtral-8x7B (strong reasoning)": "mixtral-8x7b-32768",
    "Gemma-2-9B (clean tone)": "gemma2-9b-it",
}
MODEL_NAME = MODEL_MAP[model_choice]

# -----------------------------
# CHAT PANEL (no st.chat_message, no faces)
# -----------------------------
st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    role = msg["role"]
    cls = "user" if role == "user" else "assistant"
    st.markdown(
        f"""
        <div class="msg-row {cls}">
            <div class="bubble {cls}">
                {msg["content"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# INPUT AREA
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

    # add user message
    st.session_state.messages.append({"role": "user", "content": content})

    # call Groq
    with st.spinner("XO AI is thinking..."):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}]
            + st.session_state.messages,
        )
        reply = response.choices[0].message.content

    # add assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
