import streamlit as st
from groq import Groq

# --------- CONFIG ---------
# Groq API key will come from Streamlit Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_MESSAGE = """
You are NexoBot, an AI assistant created by Nexo.corp.

Your role:
- Help with studies, motivation, basic tech/AI questions.
- Speak simple English with a little friendly Hinglish.
- Be kind, calm, supportive, and non-judgmental.

Style:
- Talk like a smart, chill older brother from India.
- Never be rude.
- Keep answers clear and not too long unless user asks.
"""

# --------- STREAMLIT UI SETUP ---------
st.set_page_config(page_title="Nexo.corp AI Chatbot", page_icon="task_01kbdc4yyres7axsn309re3k8f_1764606833_img_1")

st.title("🤖 Nexo.corp AI Chatbot")
st.write("Welcome to NexoBot!")

# Keep chat messages stored
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------- CHAT FUNCTION ---------
def get_ai_response(user_msg):
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}]

    # Add chat history
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # Add new user message
    messages.append({"role": "user", "content": user_msg})

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7
    )

    ai_msg = response.choices[0].message.content
    return ai_msg

# --------- CHAT UI ---------
user_input = st.chat_input("Type your message...")

# Show the chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# When user sends a message
if user_input:
    # Add user msg
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Get AI reply
    ai_reply = get_ai_response(user_input)

    with st.chat_message("assistant"):
        st.write(ai_reply)

    # Save reply
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
