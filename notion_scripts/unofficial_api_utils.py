from notion.client import NotionClient
import os

client = NotionClient(token_v2=os.getenv('NOTION_V2_TOKEN'))


def delete_page(page_id):
    if not page_id:
        return
    if page := client.get_block(page_id):
        page.remove()


def synchronize_select_options(projects, sections, tags):
    print('Synchronizing projects, sections, and tags ...')
    cv = client.get_collection_view(os.getenv('NOTION_TODOIST_VIEW'))
    parsed_props = {'projects': [], 'sections': [], 'tags': []}
    for prop in cv.collection.get_schema_properties():
        if prop['name'] == 'Project':
            parsed_props['projects'] = [option['value'] for option in prop.get('options', [])]
        elif prop['name'] == 'Section':
            parsed_props['sections'] = [option['value'] for option in prop.get('options', [])]
        elif prop['name'] == 'Tags':
            parsed_props['tags'] = [option['value'] for option in prop.get('options', [])]
    
    row = cv.collection.add_row()
    row.Task = "DELETE ME"
    
    for project in projects:
        if project in parsed_props['projects']:
            continue
        row.set_property('Project', project)
        row.set_property('Parent project', project)
    
    [row.set_property('Section', section) for section in sections if section in parsed_props['sections']]
    [row.set_property('Tags', tag) for tag in tags if tag in parsed_props['tags']]
    row.remove()
    
    print('Synchronizing completed !!')
    # sync Project, Parent project, Section, Tags


def synchronize_goals(goals):
    cv = client.get_collection_view(os.getenv('NOTION_GOALS_VIEW'))
    existing_db_goals = []
    for prop in cv.collection.get_schema_properties():
        if prop['name'] == 'Goal':
            existing_db_goals = [option['value'] for option in prop.get('options', [])]
            break

    row = cv.collection.add_row()
    row.Task = "DELETE ME"
    [row.set_property('Goal', goal) for goal in goals if goal not in existing_db_goals]
    row.remove()
    
    print('Synchronizing completed !!')
