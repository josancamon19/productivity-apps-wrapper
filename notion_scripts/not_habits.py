import requests
from collections import defaultdict
import datetime
from . import utils, unofficial_api_utils

database_habits = 'b5d76d7b3186427288fe545c20ce3668'


def get_today_page():
    data = {'filter': {'property': '-Date', "date": {"equals": datetime.date.today().strftime('%Y-%m-%d')}}}
    result = requests.post(f'{utils.base_url}databases/{database_habits}/query', json=data, headers=utils.headers).json()
    today_page = [task['id'] for task in result['results']]
    return today_page


def get_db_added_habits():
    data = requests.post(f'{utils.base_url}databases/{database_habits}/query', json={}, headers=utils.headers).json()
    dates = [task['properties']['-Date']['date']['start'] for task in data['results']]
    
    while cursor := data['next_cursor']:
        data = requests.post(f'{utils.base_url}databases/{database_habits}/query', json={'start_cursor': cursor, 'page_size': 100},
                             headers=utils.headers).json()
        dates += [task['properties']['-Date']['date']['start'] for task in data['results']]
    
    return dates


# noinspection PyTypeChecker
def save_habits(data: list):
    grouped = defaultdict(list)
    for task in data:
        grouped[task['date_completed'].split('T')[0]].append(task)
    
    def map_to_table(habits):
        day = []
        for habit in habits:
            if 'water' in habit['content'].lower():
                day.append('🧊 Wake up water')
            elif 'yoga' in habit['content'].lower():
                day.append('🧘🏼 Yoga')
            elif 'read' in habit['content'].lower():
                day.append('📚 Reading')
            elif 'exercise' in habit['content'].lower():
                day.append('🏃🏼 Exercise')
        
        return day
    
    already_added = get_db_added_habits()
    today = datetime.date.today().strftime('%Y-%m-%d')
    for date, habits in grouped.items():
        if date in already_added and date != today:
            continue
        
        if date == today:
            for page in get_today_page():
                unofficial_api_utils.delete_page(page)
        
        day_habits = map_to_table(habits)
        
        data = {'parent': {'type': 'database_id', 'database_id': database_habits},
                'properties': {
                    "Date": {"type": "title", "title": [{"type": "text", "text": {"content": date}}]},
                    "-Date": {"type": "date", "date": {"start": date}},
                }}
        for day_habit in day_habits:
            data['properties'][day_habit] = {"type": "checkbox", 'checkbox': True}
        result = requests.post(f'{utils.base_url}pages', json=data, headers=utils.headers)
        
        # TODO get notes only of the day and put them in the page details