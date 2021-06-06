import os

base_url = 'https://api.notion.com/v1/'
token = os.getenv('NOTION_SECRET')
headers = {"Authorization": f"Bearer {token}", 'Notion-Version': os.getenv('NOTION_API_VERSION')}


def map_text_value(value):
    return {"type": "rich_text", "rich_text": [{'type': 'text', 'text': {'content': value}}]}


def map_number_value(value):
    return {"type": "number", 'number': value}


def map_select_value(value):
    return {"type": "select", "select": {'name': value}}


def map_multi_select_value(values):
    return {"type": "multi_select", "multi_select": [{'name': value.replace('@', '')} for value in values]}

