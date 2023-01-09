import requests


def send_telegram_message(*, chat_id: str, bot_id: str, message: str) -> requests.Response:
    return requests.get(
        f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
    )
