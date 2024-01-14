import requests
import models
import json
import discord

url = "https://api.notion.com/v1/pages"

def sendListData(NOTION_API_KEY,NOTION_DB_LIST_ID,title,contributor,start,end,tag):
    data_to_be_written = {
        'parent':{
            'database_id':NOTION_DB_LIST_ID    
        },
        'properties':{
            'Title':{
                'rich_text':[
                    {
                        'text':{
                            'content':title
                        },
                        'annotations':{
                            'bold':True,
                            'italic':True,
                            'code':False,
                            'color':'purple'
                        }
                    }
                ]
            },
            
            'Contributors':{
                'title':[
                    {
                        'text':{
                            'content':contributor
                        }
                    }
                ]
            },

            'Start date':{
                'type':'date',
                'date':{
                    'start': start
                }
            },

            'End date':{
                'type':'date',
                'date':{
                    'start': end
                }
            },

            'Status':{
                'type':'checkbox',
                'checkbox':False
            },

            'Type':{
                'multi_select':[
                    {
                        'name':tag
                    }
                ]
            }
        }
    }
   
    headers = {
        'Authorization': NOTION_API_KEY,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
    }

    payload = json.dumps(data_to_be_written)
    response = requests.request('POST',url=url,headers=headers,data=payload)

    return response
        

