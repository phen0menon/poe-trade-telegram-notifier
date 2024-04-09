import asyncio
import logging
import time
from typing import List

import pyperclip

from config import AppConfig, init_app_config
from observer import PoeObserver
from telegram_api import (GetTelegramMessagesUpdate, get_telegram_messages,
                          send_telegram_message)
from utils import (extract_name_from_whisper, focus_poe_window,
                   is_poe_window_focused, send_whisper_reply_from_clipboard)

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
            ) and messages_count

            if should_notify:
                constructed_message = ""
                for message in messages:
                    username, content = message.split(":")
                    content = content.lstrip()
                    constructed_message += f"From {username}:\n{content}\n\n"

                    logger.info(f"Sending a message to chat_id={telegram_chat_id}")

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
            await asyncio.sleep(app_config["whispers_notifier_interval"])
    except Exception as e:
        logger.error(
            f"run_whispers_notifier: generic error - {str(e)}; continuing loop execution"
        )
        time.sleep(app_config["whispers_notifier_interval"])
        await run_whispers_notifier(observer, app_config, should_always_notify)
    except KeyboardInterrupt:
        logger.info("Program exited")


async def run_telegram_reply_observer(app_config: AppConfig, last_read_message_offset: int = None) -> None:
    try:
        telegram_chat_id = app_config["telegram_user_id"]
        telegram_bot_id = app_config["telegram_bot_token"]

        while True:
            updates: List[GetTelegramMessagesUpdate]  = get_telegram_messages(chat_id=telegram_bot_id, bot_id=telegram_bot_id, offset=last_read_message_offset)

            for update in updates:
                message = update.get('message')
                chat_id = message['chat']['id']

                # Skip processing messages in other chats
                if str(chat_id) != telegram_chat_id or not message.get('reply_to_message'):
                    continue

                original_message_text = message['reply_to_message']['text']
                whisper_author = extract_name_from_whisper(original_message_text)
                reply_message_text = message['text']

                whisper_reply = f'@{whisper_author} {reply_message_text}'
                pyperclip.copy(whisper_reply)

                if not is_poe_window_focused():
                    focus_poe_window()
                
                send_whisper_reply_from_clipboard()

                last_read_message_offset = update.get('update_id') + 1

            await asyncio.sleep(app_config["whispers_notifier_interval"])
    except Exception as e:
        logger.error(
            f"run_telegram_reply_observer: generic error - {str(e)}; continuing loop execution"
        )
        time.sleep(app_config["whispers_notifier_interval"])
        await run_telegram_reply_observer(app_config, last_read_message_offset)
    except KeyboardInterrupt:
        logger.info("Program exited")


async def run_activity_observer(observer: PoeObserver, app_config: AppConfig) -> None:
    try:
        while True:
            is_window_focused = is_poe_window_focused()
            observer.set_is_client_focused(is_window_focused)
            await asyncio.sleep(app_config["whispers_notifier_interval"])
    except ImportError as e:
        raise e
    except Exception as e:
        logger.error(f"run_activity_observer: generic error - {str(e)}")


async def main() -> None:
    app_config = init_app_config()

    observer = PoeObserver(app_config["log_path"])
    observer.open_log_file()

    coroutines = [
        run_whispers_notifier(observer, app_config, True),
        run_activity_observer(observer, app_config),
        run_telegram_reply_observer(app_config)
    ]

    await asyncio.gather(*coroutines)


if __name__ == "__main__":
    asyncio.run(main())
