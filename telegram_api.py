import logging
from typing import List, Optional, TypedDict

import requests

logger = logging.getLogger(__name__)


class GetTelegramMessageUpdateChat(TypedDict):
    id: int
    first_name: str
    username: str
    type: str


class GetTelegramMessageUpdateFrom(TypedDict):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str
    is_premium: bool


class GetTelegramMessageUpdateMessage(TypedDict):
    message_id: int
    chat: GetTelegramMessageUpdateChat
    date: int
    reply_to_message: Optional["GetTelegramMessageUpdateMessage"]
    text: str


class GetTelegramMessagesUpdate(TypedDict):
    update_id: int
    message: GetTelegramMessageUpdateMessage


class GetTelegramMessagesResponse(TypedDict):
    ok: bool
    result: List[GetTelegramMessagesUpdate]


def send_telegram_message(
    *, chat_id: str, bot_id: str, message: str
) -> requests.Response:
    return requests.get(
        f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
    )


def get_telegram_messages(
    *, chat_id: str, bot_id: str, offset: str
) -> List[GetTelegramMessagesUpdate]:
    url: str = f"https://api.telegram.org/bot{bot_id}/getUpdates"
    params = {"limit": 1}
    if offset:
        params["offset"] = offset

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(
            "[%s] Unable to get Telegram messages: %s", response.status_code, response
        )

    data: GetTelegramMessagesResponse = response.json()

    if data["ok"] is not True:
        raise Exception(f"Unable to get Telegram messages: {data}")

    return data["result"]
