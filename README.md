# TopSupergroupsBot
A telegram bot for telegram public groups leaderboards

<img src="../master/resources/logo/trasparencylogo.png" width="300">

## What does this bot do?
**This bot does statistics and leaderboards about public supergrous and their users.**


This bot can be added in telegram public groups. The creator of the group can set the language and some other options.
Texting the bot in private chat, you can get **statistics about you** and **groups leaderboard**. Users can choose the order of the groups by:

- number of members
- number of sent messages during the current week
- votes average (Users can vote groups)

Groups are filtered by regions.
Leaderboards are shown with beatiful pages like for a website.

## Screenshots
_The groups you can see in the following screenshots are real groups and they are created by users not related with this project, but they just added the bot in the group to take part of the leaderboard. So i don't have any responsibilities about their names or their topics._

<img src="../master/resources/screenshots/bymembers.jpg" width="200">      <img src="../master/resources/screenshots/bymessages.jpg" width="200">      <img src="../master/resources/screenshots/byvotes.jpg" width="200">      <img src="../master/resources/screenshots/aboutyou.jpg" width="200">

## Commmands

### private chat:
```
/leaderboard - check out supergroups leaderboards
/vote - vote a group
/aboutyou - get stats about you
/settings - change your settings
/feedback - send a feedback
/help - get an help command
```

### groups:
```
/settings - set group settings
/groupleaderboard - get a message containing leaderboard of users that wrotemore messages in the group during the current week (UTC)
```


## How to install:

### On Linux:

- Move to the path where you want to create the virtualenv directory
```
cd path
```
- Create a folder containing the env named `tsbenv`
```
virtualenv -p python3 tsbenv 
```
- Install the bot from the zip
```
tsbenv/bin/pip install https://github.com/91dariodev/topsupergroupsbot/archive/master.zip
```
- Run the bot. The first parameter of the command is the `config.yaml` file. Copy from the source `config.example.yaml` and create a file named `config.yaml` replacing values.
```
tsbenv/bin/topsupergroupsbot path/config.yaml
```
- To upgrade the bot:
```
tsbenv/bin/pip install --upgrade https://github.com/91dariodev/topsupergroupsbot/archive/master.zip
```
- To delete everything:
```
cd ..
rm -rf tsbenv
```
