------- 1차 --------
웹 크롤링 코드 작성
- 대상 URI : https://news.naver.com/section/105
- selector : #newsct > div.section_component.as_section_headline._PERSIST_CONTENT
- 모든 하위 링크 수집 : 'article/' 포함 대상이며 중복 시 하나만 선택, comment는 제외

------- 2차 --------
하위 링크 에서 #title_area, #dic_area 내용 수집

------- 3차 --------
수정했던 하위 링크 내용 수집을 OPENAI 프롬프트로 수정
- 같은 폴더 있는 01_openAI_chat_completions.py > chat_with_gpt() 사용
- 결과 반환은 JSON 형식