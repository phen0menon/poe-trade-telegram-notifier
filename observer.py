import logging
import re
import sys
from typing import List, Optional

from utils import get_poe_logs_path

logger = logging.getLogger(__name__)

WHISPER_MESSAGE_REGEX = re.compile("@From (.*)")
AFK_MODE_NOTIFICATION_REGEX = re.compile("AFK mode is now (.*)")


class PoeObserver:
    """
    Reads POE Client logs and parses incoming messages from it
    """

    is_client_focused = False
    is_client_afk = False

    def __init__(self, username: str, custom_log_path: Optional[str] = None):
        self.file = None
        self.logger = logger
        self.username = username

        if custom_log_path:
            self.log_path = custom_log_path
        else:
            self.log_path = get_poe_logs_path(username)
            self.logger.warning(
                "No log_path specified, trying to find default one in the [%s]",
                self.log_path,
            )

    def set_is_client_focused(self, is_client_focused: bool) -> None:
        self.is_client_focused = is_client_focused

    def open_log_file(self):
        try:
            self.file = open(self.log_path, "r", encoding="utf8")
            # traverse until EOF
            for line in self.file:
                pass
        except Exception as e:
            logging.error("Error occured while opening POE Logs file: [%s]", str(e))
            sys.exit()

    # TODO: add possibility to filter messages based on currency / count / stash tab and etc.
    def parse_whisper_messages_and_events(self):
        """
        Get incoming messages from whispers (probably POE Trade) and events (atm it's only AFK notification)
        """
        messages: List[str] = []

        for line in self.file:
            if WHISPER_MESSAGE_REGEX.search(line):
                line = WHISPER_MESSAGE_REGEX.findall(line)[0]
                # TODO: fix for i18n
                msg = line.split("(stash")[0]
                messages.append(msg)
            elif AFK_MODE_NOTIFICATION_REGEX.search(line):
                afk_mode_details = AFK_MODE_NOTIFICATION_REGEX.findall(line)[0]
                self.is_client_afk = "ON" in afk_mode_details

        return messages
