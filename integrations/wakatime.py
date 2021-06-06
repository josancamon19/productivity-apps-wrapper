from utils import get_today_str
import requests
import os

token = os.getenv('WAKATIME_API_KEY')
base_url = 'https://wakatime.com/api/v1/'


def parse_summary(day: dict):
    data = {}
    date = day['range']['date']
    data[date] = {'editors': [], 'languages': [], 'projects': [], 'total': day['grand_total']['total_seconds']}
    
    for editor in day['editors']:
        data[date]['editors'].append({'name': editor['name'], 'percent': editor['percent'], 'time_seconds': editor['total_seconds'],
                                      'time_text': editor['text']})
    
    for lang in day['languages']:
        data[date]['languages'].append({'name': lang['name'], 'percent': lang['percent'], 'time_seconds': lang['total_seconds'],
                                        'time_text': lang['text']})
    
    for project in day['projects']:
        data[date]['projects'].append({'name': project['name'], 'percent': project['percent'], 'time_seconds': project['total_seconds'],
                                       'time_text': project['text']})
    
    return data


def get_today_summary():
    tod = get_today_str()
    url = f'{base_url}users/current/summaries?api_key={token}&start={tod}&end={tod}'
    day = requests.get(url).json()['data'][0]
    return parse_summary(day)[tod]


def get_dates_summaries():
    tod = get_today_str()
    url = f'{base_url}users/current/summaries?api_key={token}&start=2021-01-01&end={tod}'
    response = requests.get(url).json()
    
    data = {}
    for day in response['data']:
        data.update(parse_summary(day))
    
    return data
