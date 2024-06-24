import requests
import json
from notion_client import Client

# Define variables for operating with the Notion API
notion_token = 'secret_xS1ntFMGfwzXxjFOnMDQuIRe0aQKneCVGChW7jydPKY'
client = Client(auth=notion_token)

# Define the URL of database you want to take the data from
# It's usually available in the public URL
database_url = 'bf687443b55f4707a49959f993389bd0'

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

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{database_url}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results

pages = get_pages()

data = []

for page in pages:
    page_id = page["id"]
    front_content = page["properties"]["Front"]["title"][0]["plain_text"].replace("<", "&lt;").replace(">", "&gt;")
    back_content = page["properties"]["Back"]["rich_text"][0]["text"]["content"]
    tag_content = page["properties"]["Tag"]["multi_select"][0]["name"]

    data.append({
        'Front': front_content,
        'Back': back_content,
        'Tag': tag_content,
    })

anki_url = 'http://localhost:8765'
deck_name = 'Omnia'
note_type = 'Omnia'

for item in data:
    note_data = {
        'action': "addNote",
        'version': 6,
        'params': {
            'note':{
                'deckName': deck_name,
                'modelName': note_type,
                'fields': {
                    'Front': item['Front'],
                    'Back': item['Back'],
                    'WordType': item['Tag']
                }
            } 
        }
    }

    response = requests.post(anki_url, json=note_data)
    response_json = json.loads(response.text)
    

    print(f"Note {item['Front']} added to Anki!")