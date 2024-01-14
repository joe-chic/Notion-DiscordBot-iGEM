import discord
import json
import requests

class SearchListData:
    id = ''
    title = ''
    start = ''
    end = ''
    status = None
    type = ''

    def __init__(self, id, title, start, end, status, type):
        self.id = id
        self.title = title
        self.start = start
        self.end = end
        self.status = status
        self.type = type

def deleteTask(NOTION_API_ID, PAGE):

    url = f'https://api.notion.com/v1/blocks/{PAGE}'

    headers = {
        "Authorization":f'Bearer {NOTION_API_ID}',
        'Notion-Version':'2022-06-28',
        'Content-Type':'application/json'
    }

    response = requests.delete(url,headers=headers)
    print(response.text,end='\n')

    if response.status_code == 200:
        return True
    else:
        return False


def getData(url,payload,headers):
    response = requests.request('POST',url=url,json=payload,headers=headers)
    print(response.text,end='\n')
    data = json.loads(response.text)
    return data

def retrieveTasks(NOTION_API_ID,NOTION_DB_ID,contributor):
    objs = []

    url = f'https://api.notion.com/v1/databases/{NOTION_DB_ID}/query'

    payload =   {
        'filter':{
            'property':'Contributors',
            'rich_text':{
                'contains':contributor
            }
        }
    }

    headers = {
            "Authorization":f'Bearer {NOTION_API_ID}',
            'Notion-Version':'2022-06-28',
            'Content-Type':'application/json'
        }

    data = getData(url=url,headers=headers,payload=payload)
    
    for row in data['results']:
        try:
            id =  row['id']
            title = row['properties']['Title']['rich_text'][0]['text']['content']
            start = row['properties']['Start date']['date']['start']
            end = row['properties']['End date']['date']['start']
            status = row['properties']['Status']['checkbox']
            type = row['properties']['Type']['multi_select'][0]['name']
            obj = SearchListData(id, title, start, end, status, type)
            objs.append(obj)
        except:
            pass

    while data['next_cursor']:
        payload = {
            'filter':{
                'property':'Contributor',
                'rich_text':{
                    'contains':contributor
                }
            },
            'start_cursor':data['next_cursor']
        }   

        data = getData(url=url,headers=headers,json=payload)
        for row in data['results']:
            try:
                id =  row['id']
                title = ['properties']['Title']['rich_text'][0]['text']['content']
                start = row['properties']['Start date']['date']['start']
                end = row['properties']['End date']['date']['start']
                stauts = row['properties']['Status']['checkbox']
                type = row['properties']['Type']['multi_select'][0]['name']
                print(title,end='\n')
                obj = SearchListData(id, title, start, end, status, type)
                objs.append(obj)
            except:
                pass
    return objs


def deleteAllCompleted(NOTION_API_ID, NOTION_DB_ID, USERS,ctx):
    
    url = f'https://api.notion.com/v1/databases/{NOTION_DB_ID}/query'

    headers = {
            "Authorization":f'Bearer {NOTION_API_ID}',
            'Notion-Version':'2022-06-28',
            'Content-Type':'application/json'
        }

    for user in USERS:
        objs = []
        payload =   {
            'filter':{
                'and':[
                    {
                        'property':'Contributors',
                        'rich_text':{
                            'contains':user
                            }
                    },
                    {
                        'property':'Status',
                        'checkbox':{
                            'equals':True
                        }
                    }
                ]
            }
        }

        data = getData(url,payload,headers)

        for row in data['results']:
            try:
                objs.append(row['id'])
            except:
                pass
    
        while data['next_cursor']:
            payload = {
                'filter':{
                    'and':[
                        {
                            'property':'Contributors',
                            'rich_text':{
                                'contains':user
                                }
                        },
                        {
                            'property':'Status',
                            'checkbox':{
                                'equals':True
                            }
                        }
                    ]
                },
                'start_cursor':data['next_cursor']
            }   

            data = getData(url=url,headers=headers,json=payload)
            for row in data['results']:
                try:
                    objs.append(row['id'])
                except:
                    pass

        no_times = 0

        for page_id in objs:
            if(not deleteTask(NOTION_API_ID ,page_id)):
                print(f'{user} couldn\'t have the task with ID:{page_id} removed.',end='\n')
            else:
                no_times += 1
         
    return (no_times == len(objs))


def getNotionUsers(NOTION_API_ID, NOTION_DB_ID, discord_members):
    url = f'https://api.notion.com/v1/databases/{NOTION_DB_ID}/query'

    headers = {
            "Authorization":f'Bearer {NOTION_API_ID}',
            'Notion-Version':'2022-06-28',
            'Content-Type':'application/json'
        }
    
    payload = {
        'filter':{
            'property':'Contributors',
            'rich_text':{
                'contains':''
            }
        }
    }

    data = getData(url,payload,headers)
    notion_members = set()

    # Discord members, should include nicknames as priority, if not, then the users.
    for row in data['results']:
        if(not(row['properties']['Contributors']['title'][0]['text']['content'] in discord_members)):
            notion_members.add(row['properties']['Contributors']['title'][0]['text']['content'])

    while data['next_cursor']:
        payload = {
            'filter':{
                'property':'Contributors',
                'rich_text':{
                    'contains':''
                }
            },
            'start_cursor':data['next_cursor']
        }

        data = getData(url,payload,headers)

        for row in data['results']:
            if(not(row['properties']['Contributors']['title'][0]['text']['content'] in discord_members)):
                notion_members.add(row['properties']['Contributors']['title'][0]['text']['content'])

    return notion_members


    


