from . import utils, unofficial_api_utils
from utils import get_today_str
import requests
import datetime
import os

database_wakatime = os.getenv('NOTION_WAKATIME_DB')


def get_today_page():
    data = {'filter': {'property': '-Date', "date": {"equals": get_today_str()}}}
    result = requests.post(f'{utils.base_url}databases/{database_wakatime}/query', json=data, headers=utils.headers).json()
    today_page = [task['id'] for task in result['results']]
    return today_page


def add_page_stats_content(page_id, content):
    if not content:
        return
    
    block = lambda text, kind: {
        "object": "block",
        "type": kind,
        kind: {
            "text": [{'type': 'text', 'text': {'content': text}}]
        }
    }
    blocks = [block('Projects', 'heading_3')]
    for project in content['projects']:
        blocks.append(block(f'{project["name"].ljust(50)}{project["time_text"].ljust(50)}{project["percent"]}%', 'paragraph'))
    
    blocks.append(block('\nEditors', 'heading_3'))
    for editor in content['editors']:
        blocks.append(block(f'{editor["name"].ljust(50)}{editor["time_text"].ljust(50)}{editor["percent"]}%', 'paragraph'))
    
    blocks.append(block('\nLanguages', 'heading_3'))
    for lang in content['languages']:
        blocks.append(block(f'{lang["name"].ljust(50)}{lang["time_text"].ljust(50)}{lang["percent"]}%', 'paragraph'))
    
    data = {'children': blocks}
    url = f'{utils.base_url}blocks/{page_id}/children'
    r = requests.patch(url, json=data, headers=utils.headers).json()
    print(r)


def get_db_added_waka_time():
    data = requests.post(f'{utils.base_url}databases/{database_wakatime}/query', json={}, headers=utils.headers).json()
    dates = [task['properties']['-Date']['date']['start'] for task in data['results']]
    
    while cursor := data['next_cursor']:
        data = requests.post(f'{utils.base_url}databases/{database_wakatime}/query', json={'start_cursor': cursor, 'page_size': 100},
                             headers=utils.headers).json()
        dates += [task['properties']['-Date']['date']['start'] for task in data['results']]
    
    return dates


def save_wakatime_data(data: dict):
    already_added = get_db_added_waka_time()
    today = get_today_str()
    for date, day_data in data.items():
        
        if date in already_added and date != today:
            continue
        
        if date == today:
            for page in get_today_page():
                unofficial_api_utils.delete_page(page)
        
        data = {'parent': {'type': 'database_id', 'database_id': database_wakatime},
                'properties': {
                    "Date": {
                        "type": "title",
                        "title": [{"type": "text", "text": {"content": date}}]
                    },
                    "Total": utils.map_number_value(day_data['total']),
                    "-Date": {
                        "type": "date",
                        "date": {"start": date}
                    },
                }}
        result = requests.post(f'{utils.base_url}pages', json=data, headers=utils.headers)
        
        print(result.json())
        
        if result.status_code >= 300:
            print(result, result.content)
            continue
        
        page_id = result.json().get('id')
        add_page_stats_content(page_id, day_data)
