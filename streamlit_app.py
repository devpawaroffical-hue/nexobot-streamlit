import streamlit as st
from groq import Groq

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(
    page_title="XO AI — Nexo.corp",
    page_icon="🤖",
    layout="wide",
)

# -------------------
# BASIC STYLES (simple + clean)
# -------------------
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #050505;
        color: #f5f5f5;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 900px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    /* header row */
    .top-title {
        font-size: 1.4rem;
        font-weight: 600;
        padding-bottom: 0.3rem;
    }

    /* make chat_input a bit darker */
    div[data-baseweb="textarea"] > textarea {
        background: #111214 !important;
        color: #ffffff !important;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------
# LLM CLIENT
# -------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
You are XO AI, an assistant created by Nexo.corp.

Tone:
- Calm, clear, mature.
- Use emojis rarely, only when they truly add value.
- No cringe or over-excited style.

Skills:
- Study help, explanations, reasoning, tech, maths, science.
- Simple, practical life and productivity advice.
- For graphs/diagrams/images, describe them in words; optionally give short Python code or image prompts.

Style:
- Short paragraphs and bullet points when helpful.
- Be honest if unsure instead of guessing.
"""

# -------------------
# STATE
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{role, content}]

def new_chat():
    st.session_state.messages = []

# -------------------
# MODEL CALL
# -------------------
def xo_reply(history):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    msgs.extend(history)
    res = client.chat.completions.create(
        model=MODEL_NAME,
        messages=msgs,
        temperature=0.4,
        max_tokens=700,
    )
    return res.choices[0].message.content.strip()

# -------------------
# HEADER (like ChatGPT top bar)
# -------------------
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.markdown('<div class="top-title">XO AI</div>', unsafe_allow_html=True)
with col2:
    if st.button("New chat"):
        new_chat()

st.divider()

# -------------------
# CHAT HISTORY (like ChatGPT)
# -------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------
# INPUT BOX (bottom, simple)
# -------------------
user_text = st.chat_input("Ask XO AI")

if user_text:
    # show user msg
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("user"):
        st.markdown(user_text)

    # get bot reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = xo_reply(st.session_state.messages)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# -------------------
# FOOTER TAG
# -------------------
st.markdown("---")
st.caption("By messaging XO AI, you agree to our Terms and Privacy Policy.")
st.caption("Founder: Dev • Nexo.corp")
