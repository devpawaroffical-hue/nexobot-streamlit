import streamlit as st
from groq import Groq

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="XO AI — Free Version",
    page_icon="🤖",
    layout="wide",
)

# ==============================
# GROQ CLIENT (FREE MODELS)
# ==============================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==============================
# SYSTEM PROMPT
# ==============================
SYSTEM_PROMPT = """
You are XO AI, an advanced professional assistant created by Nexo.corp.

Qualities:
- Mature, calm, respectful.
- Very strong at: academics, maths, coding, tech, business, psychology, productivity, daily life.
- Emotion-aware: respond with empathy first when user is upset or stressed.
- Give clear, structured answers with short paragraphs and bullet points when helpful.
- Avoid cringe or childish language.
- Prefer accuracy and honesty over guessing. If you are not fully sure, say so clearly.
- Tone similar to ChatGPT: polite, helpful, and intelligent; adjust slightly to the user’s mood.
"""

# ==============================
# SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I’m XO AI. How can I help you today?"}
    ]


def new_chat():
    st.session_state.messages = [
        {"role": "assistant", "content": "New chat started. What can XO do for you?"}
    ]


# ==============================
# STYLES (grey-black + ChatGPT-style initials)
# ==============================
st.markdown(
    """
<style>
body, .stApp {
    background: #050607;
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

/* ChatGPT-style avatar circles with initials */
[data-testid="stChatMessageAvatar"] {
    width: 32px !important;
    height: 32px !important;
    border-radius: 50% !important;
    background: #111827 !important;
    border: 1px solid #27303a !important;
    color: #e5e7eb !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* tighten spacing */
[data-testid="stChatMessage"] > div:nth-child(1) {
    margin-right: 10px !important;
}

/* chat input darker */
div[data-baseweb="textarea"] > textarea {
    background: #111214 !important;
    color: #f5f5f5 !important;
    border-radius: 8px !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==============================
# HEADER
# ==============================
col1, col2 = st.columns([0.75, 0.25])
with col1:
    st.markdown('<div class="chat-title">XO AI (Free)</div>', unsafe_allow_html=True)
with col2:
    if st.button("New chat"):
        new_chat()

st.divider()

# ==============================
# MODEL SELECTOR (all free)
# ==============================
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

# ==============================
# SHOW CHAT HISTORY (with initials avatars)
# ==============================
for msg in st.session_state.messages:
    role = msg["role"]
    # initials like ChatGPT
    avatar_initial = "XO" if role == "assistant" else "U"

    with st.chat_message(role, avatar=avatar_initial):
        st.markdown(msg["content"])

# ==============================
# USER INPUT
# ==============================
user_text = st.chat_input("Ask XO AI anything...")

if user_text:
    # store + show user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user", avatar="U"):
        st.markdown(user_text)

    # model call
    with st.chat_message("assistant", avatar="XO"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                + st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)

    # save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ==============================
# FOOTER (simple)
# ==============================
st.markdown("---")
st.caption("By using XO AI, you agree to basic Terms and Privacy practices.")
