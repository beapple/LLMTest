import streamlit as st
import openai
import os
from dotenv import load_dotenv

# load API credentials
load_dotenv()
openai.azure_endpoint = os.getenv("ENDPOINT")
openai.api_key = os.getenv("API_KEY")
openai.api_type = os.getenv("API_TYPE")
openai.api_version = os.getenv("API_VERSION")

st.set_page_config(page_title="AI Poet", layout="centered")
st.title("✍️ AI Poet Chat")

# conversation history storing subject, contents, poem
if "history" not in st.session_state:
    st.session_state.history = []

with st.form("poem_form", clear_on_submit=True):
    subject = st.text_input("시의 주제")
    contents = st.text_area("내용 (추가 설명)")
    submit = st.form_submit_button("시 생성")

if submit and subject:
    prompt = f"{subject}를 주제로 {contents}에 대한 시를 지어줘"
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1",
            temperature=0.7,
            messages=[
                {"role": "system", "content": "You are a AI Poet."},
                {"role": "user", "content": prompt},
            ],
        )
        poem = response.choices[0].message.content
    except Exception as e:
        poem = f"에러 발생: {e}"
    st.session_state.history.append({"subject": subject, "contents": contents, "poem": poem})

# display previous poems

# display previous poems
for entry in st.session_state.history:
    st.markdown(f"### 주제: {entry['subject']}")
    if entry['contents']:
        st.markdown(f"*{entry['contents']}*")
    st.markdown(entry['poem'])
    st.write("---")

if st.button("대화 초기화"):
    st.session_state.history = []
