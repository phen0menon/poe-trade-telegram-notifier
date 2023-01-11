import requests
import sys
import logging
import platform

logger = logging.getLogger(__name__)


def send_telegram_message(
    *, chat_id: str, bot_id: str, message: str
) -> requests.Response:
    return requests.get(
        f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
    )


WINDOWS_PLATFORMS = ["windows", "win32", "cygwin"]
MAC_PLATFORMS = ["mac", "darwin"]

POE_WINDOW_NAME = "Path of Exile"


def is_poe_window_focused() -> bool:
    platf = sys.platform.lower()
    if platf in WINDOWS_PLATFORMS:
        import win32gui

        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
        if active_window_name:
            return active_window_name == POE_WINDOW_NAME
        logging.error("Could not find active window")
        return False
    elif platf in MAC_PLATFORMS:
        # Source: https://stackoverflow.com/questions/5286274/front-most-window-using-cgwindowlistcopywindowinfo
        import Quartz

        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListExcludeDesktopElements
            | Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID,
        )
        for win in windows:
            if win["kCGWindowLayer"] == 0:
                window_name = "%s %s" % (
                    win[Quartz.kCGWindowOwnerName],
                    win.get(Quartz.kCGWindowName, ""),
                )
                return window_name == POE_WINDOW_NAME
        logging.error("Could not find active window")
        return False
    else:
        logger.error(
            f"sys.platform={platf} is not supported. Available platforms: {WINDOWS_PLATFORMS}, {MAC_PLATFORMS}"
        )


def get_poe_logs_path(username: str) -> str:
    is_windows = platform.system().lower() == "windows"

    if is_windows:
        return "C:/Steam/steamapps/common/Path of Exile/logs/Client.txt"

    return f"/Users/{username}/Library/Caches/com.GGG.PathOfExile/Logs/Client.txt"
