import notion_scripts
from integrations import wakatime, rescue_time, todoist

from apscheduler.schedulers.blocking import BlockingScheduler
import threading


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


def sync_apps():
    threads = [
        threading.Thread(target=todoist_sync),
        threading.Thread(target=rescue_time_sync),
        threading.Thread(target=wakatime_sync)
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]


def schedule_synchronizer():
    scheduler = BlockingScheduler(timezone='America/Bogota')
    
    scheduler.add_job(sync_apps, 'interval', hours=1, )
    scheduler.add_job(notion_scripts.day_reviews.create_day_review_page, 'cron', id='day_reviews', hour=21, minute=50)
    scheduler.start()


if __name__ == '__main__':
    sync_apps()
    # schedule_synchronizer()
