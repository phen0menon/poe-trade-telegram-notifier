# POE Trade Telegram Notifier

## Why

When you are an AFK or usually miss a whispering message from a POE trade mate, sometimes it's a shame. With this tool, you'll never miss a POE Trade whisper message if you use Telegram.

## How to install

Configure config.ini in the project root:

##### TelegramBotToken

Create telegram bot which will notify you about all incoming whispers. You can use [BotFather](https://t.me/BotFather) for creating one, it is simple stupid. Obtain created bot token. You can do that in the BotFather. The bot token usually have the following pattern: `181283218:BBFRF5r-2Q2fSofZV-wQOFXKX6UIsd_GTtl`

##### TelegramUserId 

Obtain your telegram id. You can do that using [GetMyId](https://t.me/getmyid_bot) bot

##### DirectoryUsername

Current user name of PC. Check Users folder of your system to determine which username to specify

##### LogPath

Your Path of Exile logging directory. Typically, it is located in the steam/steamapps/Path of Exile/logs/Client.txt for Windows and in /Users/{username}/Library/Caches/com.GGG.PathOfExile/Logs/Client.txt for MacOS

after filling the config.ini with your values, run the Python process:
```python
$ python3 main.py
```
