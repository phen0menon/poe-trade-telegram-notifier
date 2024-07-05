import pyautogui


def extract_name_from_whisper(whisper: str) -> str:
    part_with_name = whisper.split(":")[0]
    return part_with_name.split()[-1]


def send_whisper_reply_from_clipboard() -> None:
    pyautogui.press("enter", _pause=0.1)
    pyautogui.hotkey("ctrl", "a", _pause=0.3)
    pyautogui.hotkey("ctrl", "v", _pause=0.3)
    pyautogui.press("enter", _pause=0.1)
