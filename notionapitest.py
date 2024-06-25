import requests
import json
from notion_client import Client
from duckduckgo_search import DDGS
import os

notion_token = os.environ['NOTION_TOKEN']
client = Client(auth=notion_token)

database_url = '9a5d143036fd4a79a59a042bdf0dfbd2'

headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{database_url}/query"

    response = requests.post(url, headers=headers)

    data = response.json()

    results = data["results"]
    
    while data["has_more"]:
        payload = {"start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{database_url}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    
    words = []
    
    for item in results:
        if len(item["properties"]["Image"]["files"]) == 0:
            words.append(item["properties"]["Word"]["title"][0]["text"]["content"])

    print(f'The words found are {len(words)}.')

    return words

def get_imageurls():
    
    image_urls = []

    for word in get_pages():
        search_image = DDGS(timeout=20000).images(
            keywords=word,
            region="ge-ge",
            max_results=1,
        )
        image_urls.append(search_image[0]["image"])
    
    return image_urls

get_page = get_pages()
get_urls = get_imageurls()

final_dict = {get_page[i]: get_urls[i] for i in range(len(get_page))}

for word, url in final_dict:
    print(f"The key is {word}; the URL is {url}.")

with open('final_dict.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=4)