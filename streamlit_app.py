import os
import time
import streamlit as st
from groq import Groq

# -------------------
# PAGE CONFIG & THEME
# -------------------
st.set_page_config(
    page_title="XO AI — Nexo.corp",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS for full-black, Discord-style UI
st.markdown(
    """
    <style>
    /* Global background */
    .stApp {
        background: radial-gradient(circle at top, #050816 0, #020308 40%, #000000 100%);
        color: #f3f3f3;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Remove Streamlit default padding at top */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1.5rem;
        max-width: 1150px;
    }

    /* Chat bubbles */
    .user-bubble {
        background: #101522;
        padding: 10px 14px;
        border-radius: 16px;
        margin-bottom: 6px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .bot-bubble {
        background: #050a16;
        padding: 10px 14px;
        border-radius: 16px;
        margin-bottom: 6px;
        border: 1px solid rgba(0,255,255,0.12);
        box-shadow: 0 0 18px rgba(0,255,255,0.12);
    }

    /* Message meta text */
    .role-label {
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.55;
        margin-bottom: 2px;
    }

    /* Chat area scroll */
    .chat-container {
        max-height: 540px;
        overflow-y: auto;
        padding-right: 6px;
    }

    /* Text input bar */
    textarea {
        background-color: #060814 !important;
        border-radius: 999px !important;
    }

    /* "thinking" spinner tiny */
    .spinner-text {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-left: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------
# LLM CLIENT SETUP
# ---------------
# IMPORTANT: Set this in Streamlit secrets as GROQ_API_KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MODEL_NAME = "llama-3.1-8b-instant"  # change if you use another model

SYSTEM_PROMPT = """
You are XO AI, an advanced assistant created by Nexo.corp.

Tone & style:
- Professional, clear, and structured.
- Friendly but not cringe. Use emojis only when they truly add emotion or clarity, not in every sentence.
- Respond in concise paragraphs and bullet points when helpful.

Capabilities:
- Strong reasoning and explanation for study, tech, logic, and general topics.
- When user asks for something visual (graph, diagram, chart), explain the picture in words AND, if useful,
  provide a short Python code snippet or text description that could be used to generate a graph.
- For images, you cannot generate the image yourself, but you can:
  - describe the image in detail, and
  - output a short image prompt the user could paste into an image model.

Memory:
- You see the past messages in this conversation and should stay consistent with them.
- Do not hallucinate personal details. Clarify if you are unsure.

Safety:
- Be respectful, neutral, and supportive.
- If user is clearly sad or stressed, first acknowledge their feelings, then give calm, practical advice.
"""

# ----------------
# SESSION STATE SETUP
# ----------------
if "conversations" not in st.session_state:
    # dict: chat_id -> list of {"role": "...", "content": "..."}
    st.session_state.conversations = {}
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = "chat-1"
if st.session_state.active_chat_id not in st.session_state.conversations:
    st.session_state.conversations[st.session_state.active_chat_id] = []

def new_chat():
    chat_count = len(st.session_state.conversations) + 1
    new_id = f"chat-{chat_count}"
    st.session_state.conversations[new_id] = []
    st.session_state.active_chat_id = new_id

def switch_chat(chat_id: str):
    st.session_state.active_chat_id = chat_id

# ----------------
# MODEL CALL
# ----------------
def generate_xo_reply(messages):
    """messages: list of dicts with role: system/user/assistant + content."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.4,
        max_tokens=900,
    )
    return response.choices[0].message.content.strip()

# ---------------
# SIDEBAR = CHAT LIST / OPTIONS
# ---------------
with st.sidebar:
    st.markdown("### Nexo.corp")
    st.markdown("**XO AI – Neon Edition**")
    st.markdown(
        "<span style='font-size:0.85rem; opacity:0.75;'>Advanced conversational assistant for study, tech, reasoning & ideas.</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if st.button("➕ New chat", use_container_width=True):
        new_chat()

    st.markdown("##### Chats")
    for chat_id in sorted(st.session_state.conversations.keys()):
        label = f"Session {chat_id.split('-')[-1]}"
        if st.button(("👉 " if chat_id == st.session_state.active_chat_id else "") + label, use_container_width=True, key=f"btn-{chat_id}"):
            switch_chat(chat_id)

    st.markdown("---")
    st.markdown(
        "<span style='font-size:0.75rem; opacity:0.65;'>Tip: Ask focused questions. For graphs, say for example: <code>Plot y = x^2 from -5 to 5 and explain the shape.</code></span>",
        unsafe_allow_html=True,
    )

# ---------------
# MAIN HEADER (NO HUGE HERO)
# ---------------
col_left, col_right = st.columns([0.75, 0.25])
with col_left:
    st.markdown("#### 🤖 XO AI")
    st.markdown(
        "<span style='font-size:0.9rem; opacity:0.75;'>Designed to answer clearly, think logically, and stay calm – like a professional AI analyst.</span>",
        unsafe_allow_html=True,
    )
with col_right:
    st.markdown(
        "<div style='text-align:right; opacity:0.6; font-size:0.8rem;'>Built by <b>Nexo.corp</b></div>",
        unsafe_allow_html=True,
    )

st.markdown("")

# ---------------
# CHAT DISPLAY
# ---------------
active_messages = st.session_state.conversations[st.session_state.active_chat_id]

chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in active_messages:
        role = msg["role"]
        content = msg["content"]

        if role == "user":
            st.markdown("<div class='role-label'>You</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='user-bubble'>{content}</div>", unsafe_allow_html=True)
        elif role == "assistant":
            st.markdown("<div class='role-label'>XO AI</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bot-bubble'>{content}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------
# INPUT AREA
# ---------------
with st.form(key="chat-input", clear_on_submit=True):
    user_input = st.text_area(
        "Message XO AI...",
        placeholder="Ask about concepts, reasoning, study help, or anything you're curious about.",
        height=60,
    )
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    # Add user message
    active_messages.append({"role": "user", "content": user_input.strip()})

    # Build messages for LLM (system + history + new user)
    history_for_model = [{"role": "system", "content": SYSTEM_PROMPT}]
    history_for_model.extend(active_messages)

    # Typing indicator
    with st.spinner("XO AI is thinking..."):
        reply = generate_xo_reply(history_for_model)

    active_messages.append({"role": "assistant", "content": reply})

    # Save back
    st.session_state.conversations[st.session_state.active_chat_id] = active_messages
    st.experimental_rerun()
