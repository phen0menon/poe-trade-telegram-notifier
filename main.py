import asyncio
import time
import logging

from config import init_app_config, AppConfig
from observer import PoeObserver
from utils import is_poe_window_focused, send_telegram_message

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger.info("Started execution")


async def run_whispers_notifier(
    observer: PoeObserver, app_config: AppConfig, should_always_notify: bool = False
) -> None:
    try:
        telegram_chat_id = app_config["telegram_user_id"]
        telegram_bot_id = app_config["telegram_bot_token"]

        while True:
            messages = observer.parse_whisper_messages_and_events()
            messages_count = len(messages)
            should_notify = (
                observer.is_client_afk
                or not observer.is_client_focused
                or should_always_notify
            )
            if should_notify:
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
                        logger.info(f"Sent {messages_count} message(s) to the Telegram")
                    else:
                        logger.error(
                            f"Something went wrong while sending a request to telegram, status code: {response.status_code}"
                        )
            else:
                logger.info(
                    f"Skipping notification due to user's activity, skipped messages length={messages_count}"
                )
            await asyncio.sleep(app_config["whispers_notifier_interval"])
    except Exception as e:
        logger.error(
            f"run_whispers_notifier: generic error - {str(e)}; continuing loop execution"
        )
        time.sleep(app_config["whispers_notifier_interval"])
        await run_whispers_notifier(observer, app_config, should_always_notify)
    except KeyboardInterrupt:
        logger.info("Program exited")


async def run_activity_observer(observer: PoeObserver, app_config: AppConfig) -> None:
    try:
        while True:
            is_window_focused = is_poe_window_focused()
            observer.set_is_client_focused(is_window_focused)
            await asyncio.sleep(app_config["activity_observer_interval"])
    except ImportError as e:
        raise e
    except Exception as e:
        logger.error(f"run_activity_observer: generic error - {str(e)}")


async def main() -> None:
    app_config = init_app_config()

    observer = PoeObserver(app_config["dir_username"], app_config["log_path"])
    observer.open_log_file()

    coroutines = [
        run_whispers_notifier(observer, app_config),
        run_activity_observer(observer, app_config),
    ]

    await asyncio.gather(*coroutines)


if __name__ == "__main__":
    asyncio.run(main())
