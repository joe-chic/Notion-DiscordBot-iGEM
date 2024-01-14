import json
import requests
import discord
from functionality.database_list.deleteTask import SearchListData

def changeOneTask(NOTION_API_ID,NOTION_DB_ID, obj:SearchListData):

    url = f'https://api.notion.com/v1/pages/{obj.id}'

    headers = {
            "Authorization":f'Bearer {NOTION_API_ID}',
            'Notion-Version':'2022-06-28',
            'Content-Type':'application/json'
        }

    payload = {
        'properties':{
            'Status':{
                'checkbox':not(obj.status)
            }
        }
    }

    response = requests.request('PATCH',url=url,json=payload,headers=headers)
    print(response.text)

    if response.status_code == 200:
        return True
    else:
        return False