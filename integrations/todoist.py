from notion_scripts.unofficial_api_utils import synchronize_select_options
from utils import get_today_str
import todoist
import os

api = todoist.TodoistAPI(os.getenv('TODOIST_TOKEN'))
api.sync()

sections = {section.data.get('id'): section.data.get('name') for section in api.sections.all()}
labels = {label.data.get('id'): label.data.get('name') for label in api.labels.all()}


def parse_task_data(data: dict):
    return {'id': data['task_id'], 'content': data['content'], 'date_completed': data['completed_date'], }


def get_completed_today_tasks():
    since = get_today_str() + 'T00:00'
    completed = api.completed.get_all(since=since)
    return [parse_task_data(task) for task in reversed(completed['items'])]


def get_completed_today_habits():
    since = get_today_str() + 'T00:00'
    completed = api.completed.get_all(since=since, project_id=2266970739)
    return [parse_task_data(task) for task in reversed(completed['items'])]


def get_completed_goals_tasks():
    completed = api.completed.get_all(project_id=2254137012, since='2021-01-01T00:00')
    return [parse_task_data(task) for task in reversed(completed['items'])]


def get_goals_sections():
    return [label.data.get('name') for label in api.sections.all(filt=lambda x: x.data.get('project_id') == 2254137012)]


def get_completed_tasks_by_project_id(project_id, limit=200, since='2021-01-1T00:00'):
    completed_tasks = []
    
    completed = api.completed.get_all(project_id=project_id, limit=limit, since=since)
    completed_tasks += completed['items']
    
    while len(completed['items']) == 200:
        completed = api.completed.get_all(project_id=project_id, limit=limit, since=since, offset=len(completed_tasks))
        completed_tasks += completed['items']
    
    return [parse_task_data(task) for task in completed_tasks]


def detail_completed_tasks(completed_tasks: list):
    def parse_notes(notes: list):
        return [{'content': note.get('content'), 'created': note.get('posted')} for note in notes]
    
    def extract_details_data(data, task_name):
        if data:
            tags = [part for part in task_name.split(' ') if '@' in part]
            notes = parse_notes(data.get('notes', []))
            is_recurring = data['item'].get('due', {})
            if is_recurring is not None:
                is_recurring = is_recurring.get('is_recurring', False)
            
            section = data['item'].get('section_id')
            if section is not None:
                section = sections.get(section, '')
            else:
                section = ''
            return {'labels': data['item'].get('labels', []), 'notes': notes, 'tags': tags, 'is_recurring': is_recurring,
                    'section': section, 'date_added': data['item'].get('date_added', '')}
        return {}
    
    completed_tasks_details = []
    for task in completed_tasks:
        details = api.items.get(task['id'])
        parsed_details = extract_details_data(details, task['content'])
        task.update(parsed_details)
        completed_tasks_details.append(task)
    
    return completed_tasks_details


def get_projects():
    projects_data = api.projects.all()
    archived_projects_data = api.projects.get_archived()
    print('Projects data', len(projects_data))
    print('Archived projects data', len(archived_projects_data))
    projects = {}
    
    for project in (projects_data + archived_projects_data):
        project_id = project['id']
        parent_id = project['parent_id']
        name = project['name']
        archived = project['is_archived'] == 1
        if name == 'Inbox':
            continue
        projects[project_id] = {'name': name, 'archived': archived, 'parent_id': parent_id}
    return projects


def get_tasks_history(already_saved_tasks):
    projects = get_projects()
    
    synchronize_select_options(
        list(map(lambda proj: proj['name'], projects.values())),
        list(sections.values()),
        list(labels.values()))
    
    to_ignore = [2250617044, 2232633941, 2258542988]
    
    history = {}
    
    for project_id, project_data in projects.items():
        if project_id in to_ignore:
            print('Ignoring', project_data['name'])
            continue
        
        completed_tasks = get_completed_tasks_by_project_id(project_id)
        print(project_data['name'], 'tasks:', len(completed_tasks))
        completed_tasks = list(filter(lambda task: str(task['id']) not in already_saved_tasks, completed_tasks))
        
        completed_tasks_details = detail_completed_tasks(completed_tasks)
        
        parent = projects[project_data['parent_id']]['name'] if project_data['parent_id'] is not None else project_data['name']
        history[project_data['name']] = {'parent': parent, 'tasks': completed_tasks_details}
    return history
