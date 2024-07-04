import logging
import sys

import pyautogui

logger = logging.getLogger(__name__)


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
        return False
    elif platf in MAC_PLATFORMS:
        # Source: https://stackoverflow.com/questions/5286274/front-most-window-using-cgwindowlistcopywindowinfo
        import Quartz  # type: ignore

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
        return False
    else:
        raise Exception(
            f"sys.platform={platf} is not supported. Available platforms: {WINDOWS_PLATFORMS}, {MAC_PLATFORMS}"
        )


def focus_poe_window() -> None:
    platf = sys.platform.lower()

    if platf not in WINDOWS_PLATFORMS:
        raise Exception("NotImplemented: focus_poe_window works on Windows only")

    import win32gui
    import win32con

    hwnd = win32gui.FindWindowEx(0, 0, 0, POE_WINDOW_NAME)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)


def extract_name_from_whisper(whisper: str) -> str:
    part_with_name = whisper.split(":")[0]
    return part_with_name.split()[-1]


def send_whisper_reply_from_clipboard() -> None:
    pyautogui.press("enter", _pause=0.1)
    pyautogui.hotkey("ctrl", "a", _pause=0.3)
    pyautogui.hotkey("ctrl", "v", _pause=0.3)
    pyautogui.press("enter", _pause=0.1)
