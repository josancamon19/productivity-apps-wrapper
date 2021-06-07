from . import utils, not_habits
from utils import get_today_str
from collections import defaultdict
import requests
import datetime
import os

database_todoist = os.getenv('NOTION_TODOIST_DB')


def get_db_added_tasks_id():
    data = requests.post(f'{utils.base_url}databases/{database_todoist}/query', json={}, headers=utils.headers).json()
    ids = [task['properties']['Id']['rich_text'][0]['plain_text'] for task in data['results'] if task['properties']['Id']['rich_text']]
    
    while cursor := data['next_cursor']:
        data = requests.post(f'{utils.base_url}databases/{database_todoist}/query', json={'start_cursor': cursor},
                             headers=utils.headers).json()
        ids += [task['properties']['Id']['rich_text'][0]['plain_text'] for task in data['results']]
        print('Tasks already in db:', len(ids))
    
    return ids


def exists_task_by_id(task_id):
    data = {
        'filter': {
            'property': 'Id',
            'text': {'equals': str(task_id)}
        }
    }
    result = requests.post(f'{utils.base_url}databases/{database_todoist}/query', json=data, headers=utils.headers).json()
    return len(result['results']) > 0


def query_today_tasks():
    data = {
        'filter': {
            'property': 'Completion Date',
            "date": {"equals": get_today_str()}
        }
    }
    result = requests.post(f'{utils.base_url}databases/{database_todoist}/query', json=data, headers=utils.headers).json()
    tasks = defaultdict(list)
    
    for task in result['results']:
        props = task['properties']
        project = props['Project']['select']['name'].capitalize()
        parsed_data = {'id': task['id'], 'project': project,
                       'tags': [tag['name'] for tag in props['Tags']['multi_select']],
                       'task': props['Task']['title'][0]['text']['content']
                       }
        tasks[project].append(parsed_data)
    
    return tasks


def add_notes_to_page(page_id, notes):
    if not notes:
        return
    
    block = lambda note: {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "text": [{'type': 'text', 'text': {'content': f'{note["content"]}\n{note["created"]}\n'}}]
        }
    }
    data = {'children': [block(note) for note in notes]}
    url = f'{utils.base_url}blocks/{page_id}/children'
    requests.patch(url, json=data, headers=utils.headers).json()


# noinspection PyTypeChecker
def create_db_item(task: dict, project: str, parent_project: str):
    data = {'parent': {'type': 'database_id', 'database_id': database_todoist},
            'properties': {
                "Task": {
                    "type": "title",
                    "title": [{"type": "text", "text": {"content": task['content']}}]
                },
                "Id": utils.map_text_value(str(task['id'])),
                "Project": utils.map_select_value(str(project)),
                "Parent project": utils.map_select_value(str(parent_project)),
                "Creation Date": {
                    "type": "date",
                    "date": {"start": task.get('date_completed')}
                },
                "Completion Date": {
                    "type": "date",
                    "date": {"start": task.get('date_added')}
                }
            }}
    if task.get('section'):
        data['properties']['Section'] = utils.map_select_value(task['section'])
    if task.get('tags'):
        data['properties']['Tags'] = utils.map_multi_select_value(task['tags'])
    
    result = requests.post(f'{utils.base_url}pages', json=data, headers=utils.headers)
    
    if result.status_code >= 300:
        print(result, result.content)
        return
    
    page_id = result.json().get('id')
    add_notes_to_page(page_id, task['notes'])
    print(task, '---- added')


def save_tasks(tasks: dict):
    for project_name, data in tasks.items():
        parent, tasks = data['parent'], data['tasks']
        
        if project_name == 'Habits':
            not_habits.save_habits(tasks)
            continue
        
        elif project_name == 'Goals':
            print('GOALSSSSS', parent, tasks)
        
        for task in tasks:
            create_db_item(task, project_name, parent)
