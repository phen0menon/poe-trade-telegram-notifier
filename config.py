import logging
import sys
import configparser
from typing import Set, TypedDict, Optional


logger = logging.getLogger(__name__)

DEFAULT_WHISPERS_NOTIFIER_INTERVAL = 0.5
DEFAULT_ACTIVITY_OBSERVER_INTERVAL = 1

CONFIG_REQUIRED_SECTIONS: Set[str] = {"DEFAULT", "telegram", "directories"}


class AppConfig(TypedDict):
    telegram_bot_token: str
    telegram_user_id: str
    dir_username: str
    log_path: Optional[str]

    whispers_notifier_interval: int
    activity_observer_interval: int


def init_app_config() -> AppConfig:
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")

        for section in config.sections():
            if section not in CONFIG_REQUIRED_SECTIONS:
                raise ValueError("Missing section in config.ini: [%s]", section)

        telegram_bot_token = config["telegram"]["TelegramBotToken"]
        if not telegram_bot_token:
            raise ValueError("Missing telegram.TelegramBotToken variable in ini-config")

        telegram_user_id = config["telegram"]["TelegramUserId"]
        if not telegram_user_id:
            raise ValueError("Missing telegram.TelegramUserId variable in ini-config")

        dir_username = config["directories"]["DirectoryUsername"]
        if not dir_username:
            raise ValueError(
                "Missing directories.DirectoryUsername variable in ini-config"
            )

        log_path = config["directories"]["LogPath"] or None

        return AppConfig(
            telegram_bot_token=telegram_bot_token,
            telegram_user_id=telegram_user_id,
            dir_username=dir_username,
            log_path=log_path,
            whispers_notifier_interval=DEFAULT_WHISPERS_NOTIFIER_INTERVAL,
            activity_observer_interval=DEFAULT_ACTIVITY_OBSERVER_INTERVAL,
        )
    except ValueError as e:
        logging.error(str(e))
        sys.exit()
    except Exception as e:
        logging.warning(f"Unhandled error in init_configs: {str(e)}")
