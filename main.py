import notion_scripts
from integrations import wakatime, rescue_time, todoist

from apscheduler.schedulers.blocking import BlockingScheduler
import threading
import os


def todoist_sync():
    already_saved_tasks = notion_scripts.not_todoist.get_db_added_tasks_id()
    tasks = todoist.get_tasks_history(already_saved_tasks)
    notion_scripts.not_todoist.save_tasks(tasks)


def rescue_time_sync():
    stats = rescue_time.get_daily_data()
    notion_scripts.not_rescuetime.save_rescuetime_data(stats)


def wakatime_sync():
    stats = wakatime.get_dates_summaries()
    notion_scripts.not_wakatime.save_wakatime_data(stats)


def goals_sync():
    goals_todoist_tasks = todoist.get_completed_goals_tasks()
    notion_scripts.not_goals.save_goals_tasks(goals_todoist_tasks)


def sync_apps():
    threads = [
        threading.Thread(target=todoist_sync),
        threading.Thread(target=rescue_time_sync),
        threading.Thread(target=wakatime_sync),
        threading.Thread(target=goals_sync)
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]


def schedule_synchronizer():
    scheduler = BlockingScheduler(timezone=os.getenv('SYNC_TIMEZONE'))
    
    scheduler.add_job(sync_apps, 'interval', hours=int(os.getenv('SYNC_EVERY_HOURS')), )
    
    day_reviews_time = os.getenv('SYNC_DAY_REVIEWS_AT').split(':')
    scheduler.add_job(notion_scripts.day_reviews.create_day_review_page, 'cron', id='day_reviews', hour=int(day_reviews_time[0]),
                      minute=int(day_reviews_time[0]))
    scheduler.start()


if __name__ == '__main__':
    sync_apps()
    schedule_synchronizer()
    # notion_scripts.day_reviews.create_day_review_page()
