import streamlit as st
from dotenv import load_dotenv
import uuid
from llm import get_ai_response, get_history_retriever

st.set_page_config(page_title="소득세 챗봇", page_icon="🤖")

st.title("🤖 소득세 챗봇")
st.caption("소득세에 관련된 모든 것을 답해드립니다.")

load_dotenv()
retriever = get_history_retriever()

# 세션 초기화
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "message_list" not in st.session_state:
    st.session_state.message_list = []

# 이전 대화 출력
for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력
if user_question := st.chat_input(placeholder="소득세에 궁금한 내용들을 말해주세요"):
    # 사용자 메시지 추가
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    # AI 응답 생성
    with st.spinner("답변을 생성하는 중입니다."):
        ai_response = get_ai_response(user_question, st.session_state.session_id, retriever)
        with st.chat_message("ai"):
            ai_message = st.write_stream(ai_response)
        st.session_state.message_list.append({"role": "ai", "content": ai_message})

print(st.session_state.session_id)