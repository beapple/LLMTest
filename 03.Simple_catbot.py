# import requests
#
# result=requests.get("http://www.naver.com")
# print(result.text)

import openai
from dotenv import load_dotenv
import os
load_dotenv()

openai.azure_endpoint = os.getenv("ENDPOINT")
openai.api_key = os.getenv("API_KEY")
openai.api_type = os.getenv("API_TYPE")
openai.api_version = os.getenv("API_VERSION")

while True:

    question = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")

    if question.lower() == "exit":
        print("챗봇을 종료합니다.")
        break

    result = openai.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role":"user","content":question}
                ]
    )

    print(result.choices[0].message.content)
