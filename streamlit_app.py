# Updating the avatar removal styling in your Streamlit XO AI app
# Only avatar-removal CSS is added. Everything else remains unchanged.

import os
from typing import List, Dict
import streamlit as st
from groq import Groq

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="XO AI — Nexo.corp",
    page_icon="🤖",
    layout="wide",
)

# ---------- UPDATED CSS (avatar fully removed) ----------
CUSTOM_CSS = """
<style>
    /* Global dark theme */
    .stApp {
        background: radial-gradient(circle at top left, #151b2b 0, #050816 40%, #02010a 100%) !important;
        color: #f5f5f5 !important;
    }

    /* Remove Streamlit header */
    header[data-testid="stHeader"] { background: transparent; }

    /* REMOVE AVATAR ICONS COMPLETELY */
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* Remove avatar wrapper background */
    [data-testid="stChatMessageAvatar"] > div {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Fix chat bubble alignment after removing avatars */
    [data-testid="stChatMessage-User"] {
        margin-left: 5% !important;
        padding-left: 1rem !important;
    }

    [data-testid="stChatMessage-Assistant"] {
        margin-right: 5% !important;
        padding-right: 1rem !important;
    }

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------- MODEL MAPPING (unchanged) -------------------
MODEL_ID_MAP = {
    "llama3-8b-8192": "llama-3.1-8b-instant",
    "llama3-70b-8192": "llama-3.3-70b-versatile",
}

MODES = ["Study Helper", "Idea Generator", "Planner", "Friendly Chat"]

# ------------------- SESSION STATE -------------------
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_mode" not in st.session_state:
        st.session_state.selected_mode = "Friendly Chat"

# ------------------- PROMPTS -------------------
def get_mode_prompt(mode: str) -> str:
    base = (
        "You are XO AI, assistant of Nexo.corp. "
        "Calm, respectful, simplified explanations. "
        "No financial/trading advice. No harmful content. "
        "Short unless user asks long. "
    )

    if mode == "Study Helper":
        return base + "Break concepts step‑by‑step."
    if mode == "Idea Generator":
        return base + "Generate practical creative ideas."
    if mode == "Planner":
        return base + "Create realistic study routines and plans."
    return base + "Friendly, positive conversation."

# ------------------- MESSAGE BUILDER -------------------
def build_messages(user_input: str) -> List[Dict[str, str]]:
    system_prompt = get_mode_prompt(st.session_state.selected_mode)
    msgs = [{"role": "system", "content": system_prompt}]
    for m in st.session_state.messages:
        msgs.append({"role": m["role"], "content": m["content"]})
    msgs.append({"role": "user", "content": user_input})
    return msgs

# ------------------- GROQ CALL -------------------
def call_groq(messages: List[Dict[str, str]], ui_model: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY missing.")

    client = Groq(api_key=api_key)
    real_model = MODEL_ID_MAP.get(ui_model, ui_model)

    resp = client.chat.completions.create(
        model=real_model,
        messages=messages,
        temperature=0.4,
        max_tokens=1024,
    )
    return resp.choices[0].message.content.strip()

# ------------------- RENDER HERO -------------------
def hero():
    st.markdown(
        """
        <div style='padding:1.5rem;background:rgba(79,70,229,0.25);border-radius:1.4rem;'>
            <h1 style='margin-bottom:0.2rem;'>XO AI — Nexo Assistant</h1>
            <p style='opacity:0.8;margin-bottom:0.4rem;'>Built by Nexo.corp for students, creators & professionals.</p>
            <div style='display:flex;align-items:center;gap:6px;background:rgba(15,23,42,0.9);padding:4px 12px;border-radius:999px;width:max-content;'>
                <span style='width:8px;height:8px;background:#22c55e;border-radius:999px;'></span>
                <span>online • powered by Groq</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------- SIDEBAR MODES -------------------
def sidebar_modes():
    st.markdown("<div style='padding:1rem;background:rgba(15,23,42,0.9);border-radius:1rem;'>", unsafe_allow_html=True)
    st.subheader("Quick Modes")

    mode = st.radio("", MODES, index=MODES.index(st.session_state.selected_mode))
    st.session_state.selected_mode = mode

    st.markdown(
        f"<p style='color:#9ca3af;font-size:0.8rem;'>Mode selected: {mode}</p>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- CHAT AREA -------------------
def chat_area(selected_model: str):
    st.markdown("<div style='padding:1rem;background:rgba(15,23,42,0.95);border-radius:1rem;'>", unsafe_allow_html=True)

    for m in st.session_state.messages:
        with st.chat_message("user" if m["role"] == "user" else "assistant"):
            st.markdown(m["content"])

    user_input = st.chat_input("Ask XO AI…")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("XO AI is thinking…"):
                try:
                    msgs = build_messages(user_input)
                    reply = call_groq(msgs, selected_model)
                except Exception as e:
                    st.error("XO AI hit a limit. Try again.")
                    st.caption(str(e))
                    return
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------- MAIN -------------------
def main():
    init_state()
    hero()

    with st.expander("Model Settings"):
        model = st.radio(
            "Choose Groq model",
            ["llama3-8b-8192", "llama3-70b-8192"],
            index=1,
            horizontal=True,
        )

    left, right = st.columns([1.9, 1.1])
    with left:
        chat_area(model)
    with right:
        sidebar_modes()

    st.markdown("<p style='text-align:center;color:#6b7280;margin-top:1rem;'>Powered by Groq • XO AI © Nexo.corp</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
