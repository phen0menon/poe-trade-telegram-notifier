# POE Trade Telegram Notifier


## Why

Since there is no auction-like mechanism in Path of Exile, trading system becomes a complex thing: you always have to be near your PC to accept trade offers. 

This application solves one major problem: when you are an AFK (but with your phone at a hand), you're always aware of what trade offers are coming to you via whispers. Moreover, you can reply to them via Telegram Messenger!

## How to install

### Prerequisites

1. System: Windows, MacOS not tested 
2. Python >= 3.8

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