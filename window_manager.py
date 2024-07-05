import sys
import logging

logger = logging.getLogger(__name__)

WINDOWS_PLATFORMS = ["windows", "win32", "cygwin"]
MAC_PLATFORMS = ["mac", "darwin"]
POE_WINDOW_NAME = "Path of Exile"


class WindowManager:
    def set_foreground(self) -> None:
        import win32gui
        # import win32con
        import win32com.client

        self._handle = win32gui.FindWindowEx(0, 0, 0, POE_WINDOW_NAME)

        if not self._handle:
            logger.warn(f"Window not found: {self._handle}")
            return

        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")
        # win32gui.ShowWindow(self._handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self._handle)

    def is_poe_window_focused(self) -> bool:
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
