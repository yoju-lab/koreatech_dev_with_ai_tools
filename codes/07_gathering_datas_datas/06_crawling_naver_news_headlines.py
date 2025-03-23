import requests
from bs4 import BeautifulSoup
import json
from openAI_chat_completions import chat_with_gpt

# Define the target URL and selector
url = 'https://news.naver.com/section/105'
selector = '#newsct > div.section_component.as_section_headline._PERSIST_CONTENT'

# Send a request to the URL
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the news items using the selector
news_items = soup.select(selector)

# Extract the required information
news_data = set()
for item in news_items:
    links = item.find_all('a')
    for link in links:
        href = link['href']
        if 'article/' in href and 'comment' not in href:
            news_data.add(href)

# Function to extract title and content from a news article using OpenAI
def extract_article_data_with_gpt(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.select_one('#title_area').get_text(strip=True) if soup.select_one('#title_area') else None
    content = soup.select_one('#dic_area').get_text(strip=True) if soup.select_one('#dic_area') else None
    prompt = f"Extract the title and content from the following HTML:\nTitle: {title}\nContent: {content}"
    result = chat_with_gpt(prompt)
    return result

# Collect the news data with title and content using OpenAI
collected_data = []
for link in news_data:
    article_data = extract_article_data_with_gpt(link)
    collected_data.append({'link': link, 'data': article_data})

# Save the collected news data in JSON format
with open('summary_news.json', 'w', encoding='utf-8') as f:
    json.dump(collected_data, f, ensure_ascii=False, indent=4)
