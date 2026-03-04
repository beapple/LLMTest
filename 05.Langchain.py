from langchain_openai import AzureChatOpenAI 
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage 
import os
from dotenv import load_dotenv
import tiktoken tokenizer = tiktoken.get_encoding('cl100k_base')  

# .env 파일에서 환경변수 로드
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader

# 환경변수에서 설정 가져오기 (기본값 제공)
MODEL_DEPLOYMENT_NAME = os.getenv('MODEL_DEPLOYMENT_NAME', 'gpt-4.1')


llm = AzureChatOpenAI(
        deployment_name=MODEL_DEPLOYMENT_NAME,                        
        temperature=1,                        
)  

messages = [
         SystemMessage(content='당신은 업무 계획을 세워주는 업무 플래너 머신입니다. 사용자의 업무를 입력 받으면 이를 위한 계획을 작성합니다.'),     
         HumanMessage(content='신입사원 교육을 해야됩니다.') 
]  


loader = PyPDFLoader('/workspaces/LLMTest/Owners_Manual.pdf') 
pages = loader.load_and_split()



def tiktoken_len(text):
    tokens = tokenizer.encode(text)   
    return len(tokens)

# answer = llm.invoke(messages) 
# print(answer.content)
