import streamlit as st
import openai
import os
from dotenv import load_dotenv

# load credentials from .env
load_dotenv()
openai.azure_endpoint = os.getenv("ENDPOINT")
openai.api_key = os.getenv("API_KEY")
openai.api_type = os.getenv("API_TYPE")
openai.api_version = os.getenv("API_VERSION")

st.set_page_config(page_title="Chatbot", layout="centered")

st.title("💬 Chat Interface")

# initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")

# input form for user
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("메시지를 입력하세요")
    submitted = st.form_submit_button("전송")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1",
            messages=st.session_state.messages,
            temperature=0.7,
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = f"에러 발생: {e}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.experimental_rerun()

# reset conversation button
if st.button("대화 초기화"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.experimental_rerun()
