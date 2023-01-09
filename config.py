import logging
import sys
import configparser
from typing import Set, TypedDict


logger = logging.getLogger(__name__)

DEFAULT_OBSERVER_COOLDOWN_SECS = 0.5
CONFIG_REQUIRED_SECTIONS: Set[str] = {"DEFAULT", "telegram", "directories"}


class AppConfig(TypedDict):
    telegram_bot_token: str
    telegram_user_id: str
    dir_username: str
    observer_cooldown_secs: float


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

        observer_cooldown_secs = float(
            config["DEFAULT"]["ObserverCooldownSecs"] or DEFAULT_OBSERVER_COOLDOWN_SECS
        )

        log_path = config["directories"]["LogPath"]

        return AppConfig(
            telegram_bot_token=telegram_bot_token,
            telegram_user_id=telegram_user_id,
            dir_username=dir_username,
            observer_cooldown_secs=observer_cooldown_secs,
        )
    except ValueError as e:
        logging.error(str(e))
        sys.exit()
    except Exception as e:
        logging.warning("Unhandled error in init_configs: [%s]", str(e))
