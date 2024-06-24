# NotionToAnki

This is not an "official" port of Notion to Anki. It's just a test. 

The basic operation is as follows:

There is a function that calls out a given Notion database. It returns the items in said database in a JSON format. The entries that have no corresponding images are then saved into a list. (DuckDuckGo library)[https://github.com/deedy5/duckduckgo_search] is then called to find images for each one of the list. These urls are appended to a list that is then merged into a dictionary ({image: url}). 

Missing: 
- Uploading these new entries with images (call to Anki).  

