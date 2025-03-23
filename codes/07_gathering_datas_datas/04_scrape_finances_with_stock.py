import requests
from bs4 import BeautifulSoup
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI
import re
import pandas as pd  # pandas 라이브러리 추가
import os  # 디렉토리 확인용 추가

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
client = OpenAI()

def scrape_stock_info(code="005930"):
    """네이버 금융에서 주식 정보를 스크래핑합니다."""
    url = f"https://finance.naver.com/item/main.naver?code={code}"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 오류를 발생시킵니다.
        
        soup = BeautifulSoup(response.content, 'html.parser')
        rate_info = soup.select_one("#rate_info_krx")
        
        if rate_info:
            # 텍스트 정보 추출
            stock_data = {}
            
            # 현재가 추출
            current_price = rate_info.select_one('.no_today .no_up .blind, .no_today .no_down .blind')
            if current_price:
                stock_data["현재가"] = clean_number(current_price.text)
            
            # 다른 정보 추출 (시가, 고가, 저가)
            price_data = rate_info.select('.no_info .blind')
            if len(price_data) >= 3:
                stock_data["시가"] = clean_number(price_data[0].text)
                stock_data["고가"] = clean_number(price_data[1].text)
                stock_data["저가"] = clean_number(price_data[2].text)
            
            # 거래량과 거래대금 추출
            trading_data = rate_info.select('.no_info2 .blind')
            if len(trading_data) >= 2:
                stock_data["거래량"] = clean_number(trading_data[0].text)
                stock_data["거래대금"] = clean_number(trading_data[1].text)
            
            return stock_data
        else:
            logging.warning("Could not find element with id 'rate_info_krx'")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def clean_number(text):
    """숫자 문자열에서 쉼표를 제거하고 숫자만 추출합니다."""
    return re.sub(r'[^\d.]', '', text)

def format_json(stock_data):
    """주식 데이터를 JSON 형식으로 변환합니다."""
    try:
        return json.dumps(stock_data, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"JSON formatting failed: {e}")
        return None

def summarize_with_gpt(stock_data, prompt_template):
    """GPT 모델을 사용하여 주식 정보를 분석합니다."""
    try:
        json_data = json.dumps(stock_data, ensure_ascii=False)
        prompt = prompt_template.format(stock_data=json_data)

        messages = [{"role": "system", "content": "You are a helpful financial assistant."},
                    {"role": "user", "content": prompt}]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"GPT analysis failed: {e}")
        return None

if __name__ == "__main__":
    stock_code = "005930"  # 삼성전자
    stock_data = scrape_stock_info(stock_code)

    if stock_data:
        # JSON 형식으로 출력
        json_output = format_json(stock_data)
        if json_output:
            print("주식 정보:")
            print(json_output)

            # DataFrame으로 변환하여 CSV로 저장
            try:
                # 데이터를 단일 행 DataFrame으로 변환
                df = pd.DataFrame([stock_data])
                
                # 저장할 디렉토리 확인 및 생성
                output_dir = 'stock_data'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                
                # CSV 파일로 저장 (파일명에 주식코드와 날짜 포함)
                csv_filename = f"{output_dir}/stock_{stock_code}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
                df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
                print(f"주식 데이터가 {csv_filename}에 저장되었습니다.")
            except Exception as e:
                logging.error(f"CSV 저장 중 오류 발생: {e}")

            # 추가적으로 GPT로 분석을 원한다면 아래 코드 주석 해제
            # analysis_prompt = """
            # 다음 주식 데이터를 분석하고 간단한 투자 조언을 제공해주세요:
            # {stock_data}
            # """
            # analysis = summarize_with_gpt(stock_data, analysis_prompt)
            # if analysis:
            #     print("\nGPT 분석:")
            #     print(analysis)
        else:
            print("JSON 변환 실패.")
    else:
        print("주식 정보 스크래핑 실패.")
