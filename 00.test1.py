from langchain_openai import AzureChatOpenAI  
from dotenv import load_dotenv
import os
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

load_dotenv()

MODEL_DEPLOYMENT_NAME = "gpt-4.1" # 실제 Azure 배포명을 입력하세요
EMBEDDING_MODEL_NAME = 'text-embedding-3-large'

from langchain_openai import AzureOpenAIEmbeddings  
embedding_model = AzureOpenAIEmbeddings(
                        azure_deployment=EMBEDDING_MODEL_NAME, 
                        chunk_size=1000)

examples = {
         "안녕하세요",     
         "제 이름은 홍길동 입니다.",     
         "이름이 무엇인가요?",     
         "랭체인은 유용합니다. ",
         "Hello World" 
         }  

embeddings = embedding_model.embed_documents(examples)

from numpy import dot
from numpy.linalg import norm
import numpy as np

def cos_sim(A,B):
  # 두 벡터 사이의 각도를 계산하여 1에 가까울수록 의미가 비슷하다고 판별합니다.
  return dot(A,B)/(norm(A)*norm(B))

print(cos_sim(embeddings[0], embeddings[1]))
# 질문과 문서 뭉치 중 1번 인덱스 문장의 유사도를 구합니다.

print(cos_sim(embeddings[0], embeddings[2]))
# 질문과 문서 뭉치 중 2번 인덱스 문장의 유사도를 구합니다.