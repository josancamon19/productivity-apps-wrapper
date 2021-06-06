from . import utils, not_todoist
from integrations import rescue_time, wakatime, todoist
import json
import requests
import datetime
import os

day_reviews_db = os.getenv('NOTION_DAY_REVIEWS_DB')

block = lambda text, kind: {
    "object": "block",
    "type": kind,
    kind: {"text": [{'type': 'text', 'text': {'content': text}}]}
}


def get_db_day_reviews():
    data = requests.post(f'{utils.base_url}databases/{day_reviews_db}/query', json={}, headers=utils.headers).json()
    for page in data['results']:
        page_id = page['id']
        props = page['properties']
    print(json.dumps(data, indent=4))


def set_day_review_questions(blocks):
    blocks.append(block('Day review  🌟', 'heading_3'))
    
    questions = ['Did you do all what you planned for your day? Yes | No',
                 'Did you do important or just busy? Important | Busy',
                 'Did something unexpected changed the planing? if so, how that affected?'
                 'What went well?',
                 'What didnt go well?', ]
    
    for question in questions:
        blocks.append(block(f'\n{question}', 'paragraph'))
        blocks.append(block('', 'paragraph'))
    
    blocks.append(block('\n\n\n', 'paragraph'))


def clean_task_name(task: str):
    return ' '.join([word for word in task.split(' ') if '@' not in word])


def set_todoist_blocks(blocks):
    blocks.append(block('Tasks completed  ✅', 'heading_3'))
    tasks = not_todoist.query_today_tasks()
    for project, tasks in tasks.items():
        blocks.append(block(f'\n{project}\t({len(tasks)})', 'paragraph'))
        for task in tasks:
            blocks.append(block(f'{clean_task_name(task["task"])}', 'paragraph'))


def set_habits_blocks(blocks):
    blocks.append(block('', 'paragraph'))
    habits = todoist.get_completed_today_habits()
    blocks.append(block('Habits 🔝', 'heading_3'))
    for habit in habits:
        blocks.append(block(f'{clean_task_name(habit["content"])}', 'paragraph'))


def set_rescuetime_blocks(blocks):
    blocks.append(block('', 'paragraph'))
    blocks.append(block('Time stats  📊', 'heading_3'))
    day_stats = rescue_time.get_today_data()
    blocks.append(block(f'Total: {day_stats["total_h"]}', 'paragraph'))
    blocks.append(block(f'Productive: {day_stats["productive_h"]}', 'paragraph'))
    blocks.append(block(f'Distracted: {day_stats["distracted_h"]}', 'paragraph'))


def set_wakatime_stats(blocks):
    blocks.append(block('', 'paragraph'))
    blocks.append(block('Coding stats  👨🏼‍💻', 'heading_3'))
    programming_stats = wakatime.get_today_summary()
    get_key_sorted = lambda key: sorted(programming_stats[key], key=lambda x: x['time_seconds'], reverse=True)
    
    languages = get_key_sorted('languages')
    projects = get_key_sorted('projects')
    
    blocks.append(block(f'\nLanguages', 'paragraph'))
    for lang in languages:
        blocks.append(block(f'{lang["name"]} \t {lang["time_text"]}', 'paragraph'))
    
    blocks.append(block(f'\nProjects', 'paragraph'))
    for project in projects:
        blocks.append(block(f'{project["name"]} \t {project["time_text"]}', 'paragraph'))


def fill_day_review_page(page_id):
    blocks = []
    
    set_day_review_questions(blocks)
    set_todoist_blocks(blocks)
    set_habits_blocks(blocks)
    set_rescuetime_blocks(blocks)
    set_wakatime_stats(blocks)
    
    data = {'children': blocks}
    url = f'{utils.base_url}blocks/{page_id}/children'
    r = requests.patch(url, json=data, headers=utils.headers).json()
    print(r)


def create_day_review_page():
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    data = {'parent': {'type': 'database_id', 'database_id': day_reviews_db},
            'properties': {
                "Name": {
                    "type": "title",
                    "title": [{"type": "text", "text": {"content": '🤔 Day retrospective'}}]
                },
                "Date": {
                    "type": "date",
                    "date": {"start": today}
                },
            }}
    result = requests.post(f'{utils.base_url}pages', json=data, headers=utils.headers)
    page_id = result.json()['id']
    fill_day_review_page(page_id)
