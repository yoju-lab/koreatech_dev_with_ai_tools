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

def get_last_page(url):
    """맨뒤 페이지 번호를 확인합니다."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        last_page = soup.select_one("td.pgRR > a")
        
        if last_page:
            return int(last_page['href'].split('=')[-1])
        else:
            logging.warning("Could not find last page element")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def scrape_naver_finance(url, page):
    """Naver Finance 페이지에서 텍스트 내용을 추출합니다."""
    try:
        response = requests.get(f"{url}&page={page}")
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        iframe = soup.select_one("iframe#day")

        if iframe:
            iframe_url = f"https://finance.naver.com{iframe['src']}"
            iframe_response = requests.get(iframe_url)
            iframe_response.raise_for_status()

            iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
            table = iframe_soup.select_one("table.type2")

            if table:
                return table.text
            else:
                logging.warning("Could not find table element in iframe")
                return None
        else:
            logging.warning("Could not find iframe element")
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
    url = "https://finance.naver.com/item/sise.naver?code=005930"
    last_page = get_last_page(url)

    if last_page:
        for page in range(1, last_page + 1):
            scraped_text = scrape_naver_finance(url, page)

            if scraped_text:
                # 날짜, 종가, 전일비, 시가, 고가, 저가, 거래량 추출 프롬프트
                summary_prompt_template = """
                다음 텍스트에서 날짜, 종가, 전일비, 시가, 고가, 저가, 거래량 정보를 JSON 형식으로 추출해주세요.
                {text}
                JSON 형식 예시:
                [
                    {{
                        "날짜": "...",
                        "종가": "...",
                        "전일비": "...",
                        "시가": "...",
                        "고가": "...",
                        "저가": "...",
                        "거래량": "..."
                    }},
                    ...
                ]
                json은 출력되지 않게 작성.
                """
                summary = summarize_with_gpt(scraped_text, summary_prompt_template)

                if summary:
                    print(f"Page {page} summary:")
                    print(summary)
                else:
                    print(f"Page {page} 요약 실패.")
            else:
                print(f"Page {page} 스크래핑 실패.")
    else:
        print("맨뒤 페이지 정보를 가져오지 못했습니다.")
