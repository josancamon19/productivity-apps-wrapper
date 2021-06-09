# Productivity apps wrapper

This project aims to be a wrapper for some common productivity apps that I use in my everyday basis. This project is the result of my
interest on doing this, and the poor integrations made by [zapier.com](http://zapier.com/) and [automate.io](http://automate.io/).

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

## Screenshots

Image             |  Explanation
-------------------------|-------------------------
![Main](screenshots/main_notion_page.png) | This is the main page wrapping the following next pages shown here below
![Day reviews](screenshots/day_reviews.png) |
![Habits](screenshots/habit_tracker.png) |
![Todoist tasks](screenshots/todoist_tasks.png) |
![Programming stats](screenshots/wakatime_stats.png) |
![Details](screenshots/wakatime_stats_details.png) |

## Setting up your own instance

### Notion setup

### Code setup

### Deployment setup

## TODOs

- Integrate Apple Health data (Sleep too)
- Integrate with apple fit data
- Page details as tables instead of ```\t``` separated strings

## FAQ

## License