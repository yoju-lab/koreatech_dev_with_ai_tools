03_scrape_wikipedia_and_summarize.py

참조 파일 참조해 웹 스크래핑 작성
- 같은 폴더에 유사 파일명으로 코드 저장

[웹 스크래핑]
- 대상 URI : https://finance.naver.com/item/sise.naver?code=005930
- 내부 iframe 구성
 + #content > div.section.inner_sub > iframe:nth-child(4)
 + 페이징 예제 : https://finance.naver.com/item/sise_day.naver?code=005930&page=1
- 페이지마다 logging debug 레벨 진행 출력

[OPENAI 프롬프트]
- 페이지 결과 text에 적용
- 날짜,	종가,	전일비,	시가,	고가,	저가,	거래량 정보를 JSON으로 반환

 + 맨뒤 버튼 : body > table.Nnavi > tbody > tr > td.pgRR > a
- 맨뒤 마지막 페이지 정보까지 모두 수집

AI 이용한 웹 스크래핑 구현
- 같은 폴더에 유사 파일명으로 코드 저장
- 대상 URI : https://finance.naver.com/item/sise.naver?code=005930
- 대상 URI 내부 iframe : 일별 시세 부분

[구현 순서]
- 맨뒤 페이지 정보 확인
- request content 가져와 openai로 프롬프트로 넘기기
- 프롬프트로 날짜,	종가,	전일비,	시가,	고가,	저가,	거래량 정보를 JSON으로 반환