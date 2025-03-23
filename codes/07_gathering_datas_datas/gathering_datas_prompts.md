## 프롬프트 모음

### 01_openAI_chat_completions.py

이 프롬프트는 OpenAI의 GPT 모델을 사용하여 웹 스크래핑과 웹 크롤링의 공통점과 차이점을 설명하는 데 사용됩니다.

```python
user_prompt = "웹 스크래핑과 웹 크롤링 공통점과 차이점 예를 들어 자세히 설명"
```

### 02_scrape_wikipedia.py

이 파일은 위키백과 페이지에서 특정 내용을 스크래핑하는 데 사용되며, 별도의 프롬프트는 사용되지 않았습니다. 스크래핑할 URL은 다음과 같습니다.

```python
url = "https://ko.wikipedia.org/wiki/%EA%B9%83%ED%97%88%EB%B8%8C_%EC%BD%94%ED%8C%8C%EC%9D%BC%EB%9F%BF"
```

### 03_scrape_wikipedia_and_summarize.py

이 프롬프트는 위키백과에서 스크랩한 텍스트를 요약하고, 역사, 특징, 중요 키워드를 추출하는 데 사용됩니다.

```python
summary_prompt_template = """
다음 텍스트에서 요약, 역사, 특징, 중요 키워드를 추출해주세요:
{text}
"""
```

