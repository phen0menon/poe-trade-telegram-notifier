import configparser
import logging
import sys
from typing import Dict, Optional, Set, TypedDict

logger = logging.getLogger(__name__)


CONFIG_REQUIRED_SECTIONS: Set[str] = {"default", "telegram", "directories"}


class AppConfig(TypedDict):
    telegram_bot_token: str
    telegram_user_id: str
    log_path: Optional[str]
    whispers_notifier_interval: float
    telegram_polling_interval: float


CONFIG_REQUIRED_FIELDS_MAP: Dict[str, str] = {
    "telegram.TelegramBotToken": "telegram_bot_token",
    "telegram.TelegramUserId": "telegram_user_id",
    "directories.LogPath": "log_path",
    "default.ObserverCooldownSecs": "whispers_notifier_interval",
    "default.TelegramPollingCooldownSecs": "telegram_polling_interval",
}

REQUIRED_FIELDS_TYPES_OVERRIDE = {
    "whispers_notifier_interval": float,
    "telegram_polling_interval": float,
}


def get_tree_value_or_exception(config: configparser.ConfigParser, key: str) -> str:
    section, field = key.split(".")
    try:
        return config[section][field]
    except:
        raise ValueError(f"Missing {key} variable in ini-config")


def init_app_config() -> AppConfig:
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")

        for section in config.sections():
            if section not in CONFIG_REQUIRED_SECTIONS:
                raise ValueError("Missing section in config.ini: [%s]", section)

        app_config = AppConfig()

        for field in CONFIG_REQUIRED_FIELDS_MAP.keys():
            value = get_tree_value_or_exception(config, field)
            alias = CONFIG_REQUIRED_FIELDS_MAP[field]
            # Cast to specific type if needed
            if alias in REQUIRED_FIELDS_TYPES_OVERRIDE:
                value = REQUIRED_FIELDS_TYPES_OVERRIDE[alias](value)
            app_config[alias] = value
        
        return app_config

    except ValueError as e:
        logging.error(str(e))
        sys.exit()
    except Exception as e:
        logging.warning(f"Unhandled error in init_configs: {str(e)}")
