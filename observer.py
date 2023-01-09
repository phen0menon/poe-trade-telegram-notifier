import logging
import re
import sys
import platform
from typing import List, Optional

logger = logging.getLogger(__name__)


class PoeObserver:
    """
    Reads POE Client logs and parses incoming messages from it
    """

    def __init__(self, username: str, custom_log_path: Optional[str] = None):
        self.file = None
        self.logger = logger
        self.username = username

        is_windows = platform.system().lower() == 'windows'
        if custom_log_path:
            self.log_path = custom_log_path
        else:
            if is_windows:
                self.log_path = (
                    "C:/Steam/steamapps/common/Path of Exile/logs/Client.txt"
                )
            else:
                self.log_path = f"/Users/{self.username}/Library/Caches/com.GGG.PathOfExile/Logs/Client.txt"
            self.logger.warning(
                "No log_path specified, trying to find default one in the [%s]",
                self.log_path,
            )

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
    def get_whisper_messages(self):
        """
        Get incoming messages from whisper (probably from POE Trade)
        """
        messages: List[str] = []

        for line in self.file:
            regex_msg = re.compile("@From (.*)")
            if regex_msg.search(line):
                messages.append(regex_msg.findall(line)[0])

        return messages
