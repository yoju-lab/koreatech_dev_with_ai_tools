import requests
from bs4 import BeautifulSoup

url = "https://ko.wikipedia.org/wiki/%EA%B9%83%ED%97%88%EB%B8%8C_%EC%BD%94%ED%8C%8C%EC%9D%BC%EB%9F%BF"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.select_one("#content")

    if content:
        print(content.text)
    else:
        print("Could not find element with id 'content'")
else:
    print(f"Request failed with status code {response.status_code}")
