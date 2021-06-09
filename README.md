# Productivity apps wrapper

This project aims to be a wrapper for some common productivity apps that I use in my everyday basis. This project is the result of me
wanting to find a way for looking at all my productivity data, and having to do it on my own due to the poor integrations made
by [zapier.com](http://zapier.com/) and [automate.io](http://automate.io/).

It aims to help you do understand what you get done every day, keep track of it, get valuable statistics out of your daily performance, and
performing even better on your next day.

### Apps wrapped

- [Todoist](http://todoist.com/) for tasks management
    - Habits project independently
    - Goals project independently
- [RescueTime](http://rescuetime.com/) for passive time tracking
- [Wakatime](http://wakatime.com/) (IDE's plugin for programming time tracking)


- [Notion](https://www.notion.so/) as the place where the data of the previous 3 resides.

### Tools used

- [Todoist API](https://developer.todoist.com/sync/v8/)
- [RescueTime API](https://www.rescuetime.com/apidoc) (Special thanks to the [@rescue_time]() team, who helped me with API fixes for this)
- [WakaTime API](https://wakatime.com/developers)
- Notion new Beta [official API](https://developers.notion.com/)
- Notion [Unofficial python API](https://github.com/jamalex/notion-py) (without this I also could've not achieved this project)
- [Heroku](https://dashboard.heroku.com/) for deploying the app as is the simplest and quickest I found

## Screenshots 📸

Image             |  Explanation
-------------------------|-------------------------
![Main](screenshots/main_notion_page.png) | This is the main page wrapping the following next pages shown here below

![Day reviews](screenshots/day_reviews.png)

![Habits](screenshots/habit_tracker.png)

![Todoist tasks](screenshots/todoist_tasks.png)

Database             |  Details
-------------------------|-------------------------
![Programming stats](screenshots/wakatime_stats.png) | ![Details](screenshots/wakatime_stats_details.png)

## Setting up your own instance 🚀

### Todoist setup

- Projects named ```Goals``` and one named ```Habits``` are required for the Habits and Goals pages respectively, everything else is
  dynamic.

--- 

### Notion setup

- Generate the notion token for the integration and share every page needed here with the
  integration https://developers.notion.com/docs#step-1-create-an-integration
- Get the Token v2 for the unofficial API as explained https://github.com/jamalex/notion-py#quickstart

#### You need to create a few pages:

Duplicate everything as a [Template](https://www.notion.so/josancamon19/Copy-of-Productivity-2a42742502fe410c8e875a870cf015a9)

#### Explanation

1. **Day reviews** pages (as a calendar)
2. **Projects** table with the next columns
   ![Projects columns](screenshots/todoist_tasks_columns.png)
    - ```Task``` as the title
    - ```Parent project``` as select
    - ```Project``` as select
    - ```Section``` as select
    - ```Tags``` as multi select
    - ```Creation Date``` as Date
    - ```Completion Date``` as Date
    - ```Id``` as text
3. **Goals Progress** Page:
   ![Goals columns](screenshots/goals_columns.png)
    - ```Task``` as the title
    - ```Goal``` as select (A todoist section)
    - ```Date Completion``` as Date
    - ```Id``` as number
4. **Habits** Page
   ![Habits columns](screenshots/habits_columns.png)
    - ```Date``` for the title
    - ```-``` Next columns for each habit
    - ```-Date``` for setting a Date object
5. **Daily stats** Page
   ![Daily stats columns](screenshots/daily_stats_columns.png)
    - ```Day``` for the title
    - ```Pulse``` Number column
    - ```Total hours``` Number column
    - ```Productive hours``` Number column
    - ```Distracting hours``` Number column
    - ```Neutral hours``` Number column
    - ```SWE hours``` Number column
    - ```Learning hours``` Number column
    - ```Entertainment hours``` Number column
    - ```Productivity %``` Number column (% formatted)
    - ```Distracting %``` Number column (% formatted)
    - ```Neutral %``` Number column (% formatted)
    - ```SWE %``` Number column (% formatted)
    - ```Learning %``` Number column (% formatted)
    - ```Entertainment %``` Number column (% formatted)
    - ```-Date``` for setting a Date object
    - ```Id``` as number
6. **Coding stats** Page
   ![Habits columns](screenshots/wakatime_stats_columns.png)
    - ```Date``` for the title
    - ```Total``` Seconds with total hours
    - ```-Date``` for setting a Date object

---

### Code setup

1. Install the ```requirements.txt``` with ```pip install -r requirements.txt```
2. Setting your env vars


- ```NOTION_API_VERSION```: https://developers.notion.com/reference/versioning
- ```NOTION_SECRET```: https://developers.notion.com/docs#getting-started
- ```NOTION_V2_TOKEN``` https://github.com/jamalex/notion-py#quickstart


- ```TODOIST_TOKEN```: https://developer.todoist.com/sync/v8/#authorization
- ```RESCUETIME_API_KEY```: https://www.rescuetime.com/anapi/manage
- ```WAKATIME_API_KEY```: https://wakatime.com/settings/account


- ```NOTION_TODOIST_VIEW```= The projects table page URL
- ```NOTION_TODOIST_DB```= Projects table ID (take it from the URL)
- ```NOTION_RESCUETIME_DB```= Daily Stats page id
- ```NOTION_WAKATIME_DB```= Coding stats page id
- ```NOTION_HABITS_DB```= Habit Tracker page id
- ```NOTION_DAY_REVIEWS_DB```= Day Review page ID
- ```NOTION_GOALS_VIEW```= Goals Progress page URL
- ```NOTION_GOALS_DB```= Goals Progress ID

3. Update the ```example.env``` file and fill it with the variables
   ```dotenv
   NOTION_API_VERSION=2021-05-13
   NOTION_SECRET=
   NOTION_V2_TOKEN=
   
   TODOIST_TOKEN=
   RESCUETIME_API_KEY=
   WAKATIME_API_KEY=
   
   NOTION_TODOIST_VIEW=
   NOTION_TODOIST_DB=
   NOTION_RESCUETIME_DB=
   NOTION_WAKATIME_DB=
   NOTION_HABITS_DB=
   NOTION_DAY_REVIEWS_DB=
   NOTION_GOALS_VIEW=
   NOTION_GOALS_DB=
   ```
4. Activate env vars with ```source example.env```

---

### Deployment setup

- Create a heroku account
- Set billing for the account (you'll spend $0 hosting this application)
- Create an app
- Set the Buildpack to heroku/python
- Add the git remote from heroku
- Push to the remote

## TODOs

- Integrate Apple Health data (Sleep too)
- Integrate with apple fit data
- Page details content as tables instead of ```\t``` separated strings

## FAQ

## License