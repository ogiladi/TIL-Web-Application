# TIL (Today I Learned) Web App
A python program that uses PRAW (The Python Reddit API Wrapper, https://praw.readthedocs.io/en/latest/), takes a random post from Reddit's today I learned (TIL) subreddit (https://www.reddit.com/r/todayilearned/) and returns the title in a more reader friendly form. The data is stored on a data base and updated periodically.

To try the app, run "python manage.py runserver". On the login page, the user should enter a client id and a client secret, which can be obtained by registering the app on reddit: https://www.reddit.com/prefs/apps/. 
