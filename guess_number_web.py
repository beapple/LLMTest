import random
import streamlit as st

st.set_page_config(page_title="숫자 맞추기 게임", layout="centered")

st.title("🎮 1부터 100까지 숫자 맞추기 게임")

# 초기화
if "number" not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.message = ""
    st.session_state.game_over = False


def reset_game():
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.message = ""
    st.session_state.game_over = False


# 게임 설명
st.write("1부터 100 사이의 숫자를 맞춰보세요!")

# 숫자 입력
guess = st.number_input("숫자를 입력하세요", min_value=1, max_value=100, step=1)

# 확인 버튼
if st.button("확인", disabled=st.session_state.game_over):
    st.session_state.attempts += 1
    if guess < st.session_state.number:
        st.session_state.message = "📉 너무 작아요."
    elif guess > st.session_state.number:
        st.session_state.message = "📈 너무 커요."
    else:
        st.session_state.message = f"🎉 정답입니다! {st.session_state.attempts}번 만에 맞추셨네요!"
        st.session_state.game_over = True

# 메시지 출력
if st.session_state.message:
    if st.session_state.game_over:
        st.success(st.session_state.message)
    else:
        st.info(st.session_state.message)

# 새 게임 버튼
if st.button("새 게임"):
    reset_game()
    st.rerun()
