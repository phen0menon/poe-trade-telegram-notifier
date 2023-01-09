import time
import logging

from config import init_app_config, AppConfig
from observer import PoeObserver
from utils import send_telegram_message

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger.info("Started execution")


def run_observer_loop(observer: PoeObserver, app_config: AppConfig) -> None:
    try:
        telegram_chat_id = app_config["telegram_user_id"]
        telegram_bot_id = app_config["telegram_bot_token"]

        while True:
            messages = observer.get_whisper_messages()
            constructed_message = ""
            for message in messages:
                username, content = message.split(":")
                content = content.lstrip()
                constructed_message += f"From {username}:\n{content}\n\n"
                response = send_telegram_message(
                    chat_id=telegram_chat_id,
                    bot_id=telegram_bot_id,
                    message=constructed_message,
                )

                if response.status_code == 200:
                    logger.info(f"Sent {len(messages)} message(s) to the Telegram")
                else:
                    logger.error(
                        "Something went wrong while sending a request to telegram, status code: [%s]",
                        response.status_code,
                    )
            time.sleep(app_config["observer_cooldown_secs"])
    except Exception as e:
        logger.error(
            "run_observer_loop: generic error - [%s]; continuing loop execution", str(e)
        )
        time.sleep(app_config["observer_cooldown_secs"])
    except KeyboardInterrupt:
        logger.info("Program exited")


def main() -> None:
    app_config = init_app_config()

    observer = PoeObserver(app_config["dir_username"], app_config["log_path"])
    observer.open_log_file()

    run_observer_loop(observer, app_config)


if __name__ == "__main__":
    main()
