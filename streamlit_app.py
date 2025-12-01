import os
import streamlit as st
from groq import Groq

# --------- CONFIG ---------
# Groq API key will come from environment (Streamlit secrets later)
GROQ_API_KEY = GROQ_API_KEY = st.secrets.get(""GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_MESSAGE = """
You are NexoBot, an AI assistant created by Nexo.corp.

Your role:
- Help with studies, motivation, basic tech/AI questions and life doubts.
- Speak simple English with a little friendly Hinglish.
- Be kind, calm, supportive, and non-judgmental.

Style:
- Talk like a smart, chill older brother from India.
- Never be rude.
- Keep answers clear and not too long unless user asks for detail.
"""

# --------- STREAMLIT UI SETUP ---------
st.set_page_config(page_title="Nexo.corp AI Chatbot", page_icon="🤖")

st.title("🤖 NexoBot — Nexo.corp AI Chatbot")
st.caption("Ask about studies, motivation, basic tech/AI, or life. I’ll reply like a calm big brother.")

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_MESSAGE}
    ]

# Show previous messages (skip system)
for msg in st.session_state.messages[1:]:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# --------- CHAT INPUT ---------
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Groq API
    try:
        with st.chat_message("assistant"):
            with st.spinner("NexoBot is thinking..."):
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                )
                reply = chat_completion.choices[0].message.content
                st.markdown(reply)

        # Save assistant reply
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(
                "Error talking to the AI model. Check API key / limits and try again later."
            )
