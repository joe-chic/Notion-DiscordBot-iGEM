import requests
import json
from functionality.utils import *
from functionality.search import *

def patch(notion_key, payload, searchObj_toDelete):
    headers = {
        'Authorization': notion_key,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }
    url = f"https://api.notion.com/v1/pages/{searchObj_toDelete.id}" # searchObj is the title.
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response.content)

# json.dumps() converts a series of python objects into json strings. Not all objects are convertible, so you need to make sure before.

def deleteWithoutTag(searchObj_toDelete, api_key):
    payload = json.dumps({
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "Contributor": {
                "type": "title",
                "title": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "URL": {
                "url": None
            }
        }
    })
    patch(api_key, payload, searchObj_toDelete)

def deleteAll(searchObj_toDelete, api_key):
    payload = json.dumps({
        "properties": {
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "Tag": {
                "type": "multi_select",
                "multi_select": [
                    {
                        "name": " "
                    }
                ]
            },
            "Contributor": {
                "type": "title",
                "title": [
                    {
                        "text": {
                            "content": ""
                        }
                    }
                ]
            },
            "URL": {
                "url": None
            }
        }
    })
    patch(api_key, payload, searchObj_toDelete)

    # pathch function is used for deletion.