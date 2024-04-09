<h1 align="center" style="border-bottom: none">
    <b><img src="https://static-00.iconduck.com/assets.00/telegram-icon-2048x1725-i4kw83ca.png" width="30" /> PoE Trade Telegram Notifier</b>
</h1>


- 📱 <b>Productivity</b>. Every trade offer you receive is forwarded to you in Telegram
- 🛡️ <b>Safety</b>. Application doesn't inject anything in Path of Exile, thus you won't be banned
- 🏃 <b>Flexibility</b>. You can reply to every trade offer via Telegram messenger just by replying to received message!
  

## Why

In Path of Exile, the absence of an auction-like mechanism complicates the trading system. It requires players to constantly monitor trade offers while being near their PC.

This application addresses a key issue: when players are away from their PC, such as browsing TikTok on the couch, they can receive whisper messages from PoE directly to their Telegram account. 

This means a player can instantly view incoming trade offers without needing to return to their PC. Additionally, players can respond to these whispers directly through Telegram Messenger. This feature is particularly useful for avoiding interruptions, like being pulled away from TikTok for a low-value trade offer (every PoE player will agree that being distracted by 1c trading is an unproductive activity).

#### How it works

Application constantly observes log file of Path of Exile located in `Path of Exile/logs/Client.txt`. If there is Whisper message, it instantly forwards to Telegram Channel. 

To get replies to messages in the Telegram Channel, application constantly polls Telegram API for getting updates of a bot.

## How to install

### Prerequisites

1. System: Windows, MacOS not tested 
2. Python >= 3.8. You can download Python here: https://www.python.org/downloads/

### Running application

1. Open project directory and open terminal in this directory.
2. Run the command to create venv: 
    ```python
    python -m venv .venv
    ```
3. Activate the venv: 
    ```python
    .venv\Scripts\activate.bat
    ```
4. Install project dependencies: 
    ```python
    pip install -r requirements.txt
    ```
5. <b>IMPORTANT</b>: make sure you configured your `config.ini` (read section below) according to your prefs. 
6. Run the application: 
    ```python
    python main.py
    ``` 

### Configuring config.ini

Required fields - mandatory for running the application

|Field 	| Type | Required | Description   	| 
|---	|---	| --- | --- |
| TelegramBotId  	| string | <b>Yes</b> |  Create telegram bot which will notify you about all incoming whispers. You can use [BotFather](https://t.me/BotFather) for creating one, it is simple stupid. Obtain created bot token. You can do that in the BotFather. The bot token usually have the following pattern: `181283218:BBFRF5r-2Q2fSofZV-wQOFXKX6UIsd_GTtl`	|
|  TelegramUserId 	| string | <b>Yes</b> |  Obtain your telegram id. You can do that using [GetMyId](https://t.me/getmyid_bot) bot 	|
| LogPath  	| string | <b>Yes</b> |  Your Path of Exile logging directory. Typically, it is located in the `steam/steamapps/Path of Exile/logs/Client.txt` for Windows and in `/Users/{username}/Library/Caches/com.GGG.PathOfExile/Logs/Client.txt` for MacOS 	|

Other fields

|Field 	| Type | Required | Description   	| 
|---	|---	| --- | --- |
| ObserverCooldownSecs  	| float | No (default is 2.0) |  Interval between log reads. You can set it to lower value in order to get notifications as fast as it's possible (it is bound to our operating system)	|
|  TelegramPollingCooldownSecs 	| float | No (default is 1.0) |  Interval between requests to Telegram API for getting reply messages. <br /><br/> <b>IMPORTANT</b>: it is recommended to not override this variable, do that only if you know what are you doing. 	|

## Development

Future requests:
  - [ ] TBD: Filter for stashes 
  - [ ] TBD: Filter for currency