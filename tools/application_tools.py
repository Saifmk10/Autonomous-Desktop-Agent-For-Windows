import os
import time
import pygetwindow as gw

from langchain.tools import tool
from pywinauto.application import Application


@tool
def open_applications(application_name: str) -> str:
    """Open Windows desktop applications."""

    paths_browsers = {
        "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "file explorer": r"C:\Windows\explorer.exe",
    }

    paths_windows_apps = {
        "notepad": r"notepad.exe",
        "calculator": r"calc.exe",
        "command prompt": r"cmd.exe",
        "file explorer": r"explorer.exe",
        "paint": r"mspaint.exe",
        "word": r"winword.exe",
        "excel": r"excel.exe",
        "powerpoint": r"powerpnt.exe",
        "outlook": r"outlook.exe",
        "visual studio code": r"Code.exe",
        "spotify": r"Spotify.exe",
        "vlc": r"vlc.exe",
        "discord": r"Discord.exe",
        "steam": r"Steam.exe",
        "skype": r"Skype.exe",
        "zoom": r"Zoom.exe",
        "teams": r"Teams.exe",
        "slack": r"slack.exe",
        "github desktop": r"GitHubDesktop.exe",
        "postman": r"Postman.exe",
        "adobe photoshop": r"Photoshop.exe",
        "teams":os.path.expandvars(r"C:\Users\saif\AppData\Local\Microsoft\WindowsApps\ms-teams.exe"),
    }

    all_apps = {
        **paths_browsers,
        **paths_windows_apps
    }

    app_name = application_name.lower().strip()

    path = all_apps.get(app_name)

    if not path:
        return f"Application '{application_name}' not found."

    Application().start(path)
    time.sleep(2)

    return f"Opened {app_name}"


@tool
def check_opened_applications(application_name: str) -> str:
    """Check if an application window is open and activate it."""
    window = gw.getWindowsWithTitle(application_name)

    if not window:
        return f"No open windows found for '{application_name}'."

    win = window[0]

    win.activate()
    win.maximize()
    win.activate()
    return f"Activated and maximized '{application_name}' window."


application_tools = [open_applications, check_opened_applications]
