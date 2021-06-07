import os

import requests
from . import utils, unofficial_api_utils, not_todoist
from integrations.todoist import get_goals_sections,detail_completed_tasks

database_goals = os.getenv('NOTION_GOALS_DB')


def get_db_added_goals():
    data = requests.post(f'{utils.base_url}databases/{database_goals}/query', json={}, headers=utils.headers).json()
    ids = [task['properties']['Id']['number'] for task in data['results']]
    
    while cursor := data['next_cursor']:
        data = requests.post(f'{utils.base_url}databases/{database_goals}/query', json={'start_cursor': cursor, 'page_size': 100},
                             headers=utils.headers).json()
        ids += [task['properties']['Id']['number'] for task in data['results']]
    
    return ids


def save_goals_tasks(tasks: list):
    already_added = get_db_added_goals()
    sections = get_goals_sections()
    print(sections)
    unofficial_api_utils.synchronize_goals(sections)
    
    for task in detail_completed_tasks(tasks):

        if task['id'] in already_added:
            continue
        
        data = {'parent': {'type': 'database_id', 'database_id': database_goals},
                'properties': {
                    "Task": {
                        "type": "title",
                        "title": [{"type": "text", "text": {"content": task['content']}}]
                    },
                    "Goal": utils.map_select_value(str(task['section'])),
                    "Date Completion": {"type": "date", "date": {"start": task['date_completed']}},
                    "Id": utils.map_number_value(task['id']),
                }}
        
        result = requests.post(f'{utils.base_url}pages', json=data, headers=utils.headers)
        
        if result.status_code >= 300:
            print(result, result.content)
            return
        
        page_id = result.json().get('id')
        not_todoist.add_notes_to_page(page_id, task['notes'])
