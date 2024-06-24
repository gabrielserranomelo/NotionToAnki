import requests
import json
from notion_client import Client

# Define variables for operating with the Notion API
notion_token = 'secret_xS1ntFMGfwzXxjFOnMDQuIRe0aQKneCVGChW7jydPKY'
client = Client(auth=notion_token)

# Define the URL of database you want to take the data from
# It's usually available in the public URL
database_url = '4e63d97b630e4bd282d6de2cd21ce8cf'

# Define headers for the requests post
headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Returns a dictionary with the database serialized as a JSON file, available in the same folder
# as "db.json"
def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{database_url}/query"

    # This is necessary for getting more than 100 pages
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

pages = get_pages()