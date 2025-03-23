import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from openai import OpenAI
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
client = OpenAI()

def scrape_wikipedia(url):
    """Wikipedia 페이지에서 텍스트 내용을 추출합니다."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 오류를 발생시킵니다.

        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.select_one("#content")

        if content:
            return content.text
        else:
            logging.warning("Could not find element with id 'content'")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def summarize_with_gpt(text, prompt_template):
    """GPT 모델을 사용하여 텍스트를 요약하거나 특정 정보를 추출합니다."""
    try:
        prompt = prompt_template.format(text=text)

        messages = [{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 또는 "gpt-4"
            messages=messages,
            temperature=0.7,
            max_tokens=500  # 필요에 따라 조정
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"GPT summarization failed: {e}")
        return None

if __name__ == "__main__":
    url = "https://ko.wikipedia.org/wiki/%EA%B9%83%ED%97%88%EB%B8%8C_%EC%BD%94%ED%8C%8C%EC%9D%BC%EB%9F%BF"
    scraped_text = scrape_wikipedia(url)

    if scraped_text:
        # 요약, 역사, 특징, 중요 키워드 추출 프롬프트
        # summary_prompt_template = """
        # 다음 텍스트에서 요약, 역사, 특징, 중요 키워드를 추출해주세요:
        # {text}
        # """
        summary_prompt_template = """
        다음 텍스트에서 요약, 역사, 특징, 중요 키워드를 JSON 형식으로 추출해주세요.
        {text}
        JSON 형식 예시:
        {{
            "요약": "...",
            "역사": "...",
            "특징": "...",
            "중요_키워드": ["...", "..."]
        }}
        json은 출력되지 않게 작성.
        """
        summary = summarize_with_gpt(scraped_text, summary_prompt_template)

        if summary:
            print("summary:")
            print(summary)
        else:
            print("요약 실패.")
    else:
        print("스크래핑 실패.")
