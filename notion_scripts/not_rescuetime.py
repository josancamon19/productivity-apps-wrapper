from . import utils, unofficial_api_utils
from utils import get_today_str
import requests
import datetime
import os

database_rescue_time = os.getenv('NOTION_RESCUETIME_DB')


def get_db_added_rescue_time():
    data = requests.post(f'{utils.base_url}databases/{database_rescue_time}/query', json={}, headers=utils.headers).json()
    ids = [task['properties']['Id']['number'] for task in data['results']]
    pages_id = [task['id'] for task in data['results']]
    while cursor := data['next_cursor']:
        data = requests.post(f'{utils.base_url}databases/{database_rescue_time}/query', json={'start_cursor': cursor, 'page_size': 100},
                             headers=utils.headers).json()
        
        ids += [task['properties']['Id']['number'] for task in data['results']]
        pages_id += [task['id'] for task in data['results']]
    
    return ids


def get_today_page():
    data = {'filter': {'property': 'Date', "date": {"equals": get_today_str()}}}
    result = requests.post(f'{utils.base_url}databases/{database_rescue_time}/query', json=data, headers=utils.headers).json()
    today_page = [task['id'] for task in result['results']]
    return today_page


def add_page_stats_content(page_id, applications):
    if not applications:
        return
    
    block = lambda text, kind: {
        "object": "block",
        "type": kind,
        kind: {
            "text": [{'type': 'text', 'text': {'content': text}}]
        }
    }
    blocks = [block('Source\tTime (min)\n', 'paragraph')]
    for category, apps in applications.items():
        blocks.append(block(f'\n{category}', 'paragraph'))
        for app in apps:
            blocks.append(block(f'{app["app"]}\t{int(app["time_seconds"] / 60)}', 'paragraph'))
    
    data = {'children': blocks}
    url = f'{utils.base_url}blocks/{page_id}/children'
    r = requests.patch(url, json=data, headers=utils.headers).json()
    print(r)


# noinspection PyTypeChecker
def save_rescuetime_data(data):
    already_added = get_db_added_rescue_time()
    today = get_today_str()
    
    for day in data:
        if day['id'] in already_added and day['date'] != today:
            # print(day['id'], '--- already added')
            continue
        
        if day['date'] == today:
            print('Deleting today row', today, )
            for page in get_today_page():
                unofficial_api_utils.delete_page(page)
        
        data = {'parent': {'type': 'database_id', 'database_id': database_rescue_time},
                'properties': {
                    "Day": {
                        "type": "title",
                        "title": [{"type": "text", "text": {"content": day['date']}}]
                    },
                    "Pulse": utils.map_number_value(day['pulse']),
                    "Total hours": utils.map_number_value(day['total_h']),
                    "Productive hours": utils.map_number_value(day['productive_h']),
                    "Distracting hours": utils.map_number_value(day['distracted_h']),
                    "Neutral hours": utils.map_number_value(day['neutral_h']),
                    "SWE hours": utils.map_number_value(day['sw_dev_h']),
                    "Learning hours": utils.map_number_value(day['learning_h']),
                    "Entertainment hours": utils.map_number_value(day['entertainment_h']),
                    "Productive %": utils.map_number_value(day['productive_%']),
                    "Distracting %": utils.map_number_value(day['distracted_%']),
                    "Neutral %": utils.map_number_value(day['neutral_%']),
                    "SWE %": utils.map_number_value(day['sw_dev_%']),
                    "Learning %": utils.map_number_value(day['learning_%']),
                    "Entertainment %": utils.map_number_value(day['entertainment_%']),
                    "Id": utils.map_number_value(day['id']),
                    "Date": {
                        "type": "date",
                        "date": {"start": day['date']}
                    },
                }}
        result = requests.post(f'{utils.base_url}pages', json=data, headers=utils.headers)
        page_id = result.json()['id']
        add_page_stats_content(page_id, day['details'])
