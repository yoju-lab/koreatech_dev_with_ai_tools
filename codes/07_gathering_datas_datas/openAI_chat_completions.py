from dotenv import load_dotenv
import os
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
client = OpenAI()

def chat_with_gpt(prompt):
    """GPT 모델과 대화하는 함수"""
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 또는 "gpt-4"
        messages=messages,
        temperature=0.7,  # 창의성 조절 (0.0에 가까울수록 결정적, 1.0에 가까울수록 무작위)
        max_tokens=150  # 응답 최대 토큰 수
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # user_prompt = input("질문을 입력하세요: ")
    user_prompt = "웹 스크래핑과 웹 크롤링 공통점과 차이점 예를 들어 자세히 설명"
    answer = chat_with_gpt(user_prompt)
    print("GPT의 응답:", answer)
