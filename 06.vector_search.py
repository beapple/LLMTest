import streamlit as st
from dotenv import load_dotenv
import os
from typing import Any, Dict

load_dotenv()

# --- 환경 설정 (필요에 따라 환경변수로 교체하세요) ---
MODEL_DEPLOYMENT_NAME = os.getenv("AZURE_LLM_DEPLOYMENT", "gpt-4.1")
EMBEDDING_MODEL_NAME = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

# --- LangChain / Chroma 임포트 ---
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_classic.chains import RetrievalQA

# LLM 및 임베딩 생성
llm = AzureChatOpenAI(deployment_name=MODEL_DEPLOYMENT_NAME, temperature=0.0)
embedding_model = AzureOpenAIEmbeddings(azure_deployment=EMBEDDING_MODEL_NAME, chunk_size=1000)

# Chroma DB 불러오기
db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_model)

# RetrievalQA 체인 생성 (retriever 설정 포함)
retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 10})
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)


def query_qa(q: str) -> Dict[str, Any]:
    """질문을 QA 체인에 전달하고 결과(응답 및 출처 문서)를 반환합니다."""
    # 여러 langchain 버전 차이를 고려해 유연하게 처리
    try:
        # 일부 버전에서는 invoke 사용
        res = qa.invoke(q)
        # invoke가 dict 형태 반환하면 사용
        if isinstance(res, dict):
            return res
        return {"result": res}
    except Exception:
        try:
            # 일반적으로 사용되는 run
            res = qa.run(q)
            return {"result": res}
        except Exception:
            try:
                # 체인을 호출형태로 사용
                res = qa({"query": q})
                if isinstance(res, dict):
                    return res
                return {"result": str(res)}
            except Exception as e:
                return {"result": f"Error: {e}"}


# --- Streamlit UI ---
st.set_page_config(page_title="Vector QA Chat", layout="wide")
st.title("Vector Search 기반 채팅")

with st.sidebar:
    st.header("설정")
    st.write("모델, 임베딩, DB 경로는 환경변수로 설정하세요.")
    if st.button("대화 초기화"):
        st.session_state.clear()


if "messages" not in st.session_state:
    st.session_state.messages = []


def add_message(role: str, content: str, sources: Any = None):
    st.session_state.messages.append({"role": role, "content": content, "sources": sources})


with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("질문 입력...")
    submit = st.form_submit_button("전송")

if submit and user_input:
    add_message("user", user_input)
    with st.spinner("검색 중..."):
        out = query_qa(user_input)
    # out는 dict로 예상: {'result': '...', 'source_documents': [...]}
    answer = out.get("result") or out.get("answer") or str(out)
    sources = out.get("source_documents") or out.get("source_docs") or out.get("source_documents")
    add_message("assistant", answer, sources)

# 채팅 출력
chat_col, src_col = st.columns([3, 1])

with chat_col:
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f"**질문:** {m['content']}")
        else:
            st.markdown(f"**응답:** {m['content']}")
        if m.get("sources"):
            with st.expander("참고 문서 보기"):
                for doc in m["sources"]:
                    try:
                        # Document 객체 형태일 때
                        text = getattr(doc, "page_content", str(doc))
                        meta = getattr(doc, "metadata", None)
                        st.write(text)
                        if meta:
                            st.caption(str(meta))
                        st.write("---")
                    except Exception:
                        st.write(str(doc))

with src_col:
    st.header("요약 정보")
    st.write("최근 질의 개수:", len(st.session_state.messages))
    st.write("DB 경로:", PERSIST_DIRECTORY)
