from utils import get_today_str, get_today
from collections import defaultdict
import requests
import json
import datetime
import os

key = os.getenv('RESCUETIME_API_KEY')
base_url = 'https://www.rescuetime.com/anapi/'


def parse_day_data(day):
    return {
        'id': day['id'],
        'date': day['date'],
        'pulse': day['productivity_pulse'],
        
        'total_h': day['total_hours'],
        'productive_h': day['all_productive_hours'],
        'distracted_h': day['all_distracting_hours'],
        'neutral_h': day['neutral_hours'],
        
        'sw_dev_h': day['software_development_hours'],
        'learning_h': day['reference_and_learning_hours'],
        'entertainment_h': day['entertainment_hours'],
        
        'productive_%': day['all_productive_percentage'],
        'distracted_%': day['all_distracting_percentage'],
        'neutral_%': day['neutral_percentage'],
        
        'sw_dev_%': day['software_development_percentage'],
        'learning_%': day['reference_and_learning_percentage'],
        'entertainment_%': day['entertainment_percentage'],
        
    }


def get_today_data():
    today = get_today_str()
    day = requests.get(f'{base_url}daily_summary_feed?key={key}&date={today}').json()[0]
    return parse_day_data(day)


def get_daily_data():
    start = datetime.date(2021, 1, 1)
    upto = get_today()
    dates = [start.strftime('%Y-%m-%d')]
    
    while (start + datetime.timedelta(days=14)) < upto:
        dates.append((start + datetime.timedelta(days=14)).strftime('%Y-%m-%d'))
        start += datetime.timedelta(days=14)
    dates.append(upto.strftime('%Y-%m-%d'))
    
    print(f'{base_url}daily_summary_feed?key={key}')
    print(dates)
    data = []
    
    for date in dates:
        response = requests.get(f'{base_url}daily_summary_feed?key={key}&date={date}')
        data += [item for item in response.json() if item['date'] not in map(lambda x: x['date'], data)]
    
    print(f'Total data received from 2021-01-01:', len(data))
    
    daily_stats = []
    for day in data:
        day_data = parse_day_data(day)
        
        url = f'{base_url}data?key={key}&interval=day&perspective=interval&restrict_begin={day["date"]}&format=json'
        details = requests.get(url).json()
        applications = defaultdict(list)
        [applications[row[4]].append({'time_seconds': row[1], 'app': row[3]}) for row in details['rows']]
        day_data['details'] = applications
        
        daily_stats.append(day_data)
    
    return daily_stats
