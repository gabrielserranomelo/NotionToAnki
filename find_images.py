from duckduckgo_search import DDGS
from notion_client import Client
import json
import requests

notion_token = 'secret_xS1ntFMGfwzXxjFOnMDQuIRe0aQKneCVGChW7jydPKY'
client = Client(auth=notion_token)

results = DDGS().images("erziehen simpsons", "ge-ge", type_image="gif", max_results=1)
    

print(results)