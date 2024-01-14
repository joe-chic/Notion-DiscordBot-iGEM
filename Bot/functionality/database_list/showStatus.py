import asyncio
import discord
import json
import requests

def showStatus(NOTION_API_KEY,NOTION_DB_LIST_ID, contributor, complete:bool):
    url = "https://api.notion.com/v1/databases/" + NOTION_DB_LIST_ID + "/query"

    headers = {
        'Authorization':'Bearer ' + NOTION_API_KEY,
        'Notion-Version':'2022-06-28',
        'Content-Type':'application/json'
    }

    payload = {
        'filter':{
            'and':[
                {
                    'property':'Status',
                    'checkbox':{
                        'equals':complete
                    }
                },
                {
                    'property':'Contributors',
                    'rich_text':{
                        'contains':contributor
                    }
                }
            ]
        }
    }

    response = requests.request('POST', url=url, headers=headers, json=payload)
    data = json.loads(response.text)
    print(response.text,end='\n')

    return data