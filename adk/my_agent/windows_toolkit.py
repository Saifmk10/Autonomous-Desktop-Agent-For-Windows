"""
Windows Toolkit for the ADK agent.

A single-file collection of plain Python functions that let the agent
control a Windows desktop: windows/apps, mouse/keyboard, filesystem,
clipboard, processes, volume and power state.

Each function is a plain callable with type hints and a docstring, which is
all google-adk's `Agent` needs to auto-wrap it as a `FunctionTool`. Just add
entries from `windows_toolkit` to an `Agent(tools=[...])` list.
"""

import os
import shutil
import subprocess
import time
import webbrowser

import pyautogui
import pygetwindow as gw
import pyperclip
from pygetwindow import PyGetWindowException
from pywinauto.application import Application

try:
    from pycaw.pycaw import AudioUtilities
    _VOLUME_AVAILABLE = True
except ImportError:
    _VOLUME_AVAILABLE = False

pyautogui.FAILSAFE = False

WORKSPACE_DIR = os.path.join(os.getcwd(), "workspace")


def _safe_window_action(action) -> None:
    """Run a pygetwindow action, ignoring the library's benign false-positive
    exception (raised even when Win32 reports success / error code 0)."""
    try:
        action()
    except PyGetWindowException as e:
        if "error code from windows: 0" not in str(e).lower():
            raise


# ---------------------------------------------------------------------------
# Window management
# ---------------------------------------------------------------------------

def list_open_windows() -> str:
    """List titles of all currently open (non-empty title) windows."""
    titles = [t for t in gw.getAllTitles() if t.strip()]
    return "\n".join(titles) if titles else "No open windows found."


def activate_window(title: str) -> str:
    """Bring the window whose title contains `title` to the foreground and maximize it."""
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        return f"No window found matching '{title}'."
    win = windows[0]
    _safe_window_action(win.activate)
    _safe_window_action(win.maximize)
    return f"Activated and maximized window: '{win.title}'"


def minimize_window(title: str) -> str:
    """Minimize the window whose title contains `title`."""
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        return f"No window found matching '{title}'."
    _safe_window_action(windows[0].minimize)
    return f"Minimized window: '{windows[0].title}'"


def close_window(title: str) -> str:
    """Close the window whose title contains `title`."""
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        return f"No window found matching '{title}'."
    win = windows[0]
    name = win.title
    _safe_window_action(win.close)
    return f"Closed window: '{name}'"


def get_active_window_title() -> str:
    """Get the title of the currently active (focused) window."""
    win = gw.getActiveWindow()
    return win.title if win else "No active window."


# ---------------------------------------------------------------------------
# Application management
# ---------------------------------------------------------------------------

_APP_PATHS = {
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "file explorer": r"C:\Windows\explorer.exe",
    "notepad": r"notepad.exe",
    "calculator": r"calc.exe",
    "command prompt": r"cmd.exe",
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
    "zoom": r"Zoom.exe",
    "teams": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\ms-teams.exe"),
    "slack": r"slack.exe",
    "github desktop": r"GitHubDesktop.exe",
    "postman": r"Postman.exe",
}


def open_application(application_name: str) -> str:
    """Open a known Windows desktop application or browser by common name (e.g. 'notepad', 'chrome')."""
    app_name = application_name.lower().strip()
    path = _APP_PATHS.get(app_name)
    if not path:
        return f"Application '{application_name}' not found in known app list."
    Application().start(path)
    time.sleep(2)
    return f"Opened {app_name}"


def close_application(process_name: str) -> str:
    """Force-close all running instances of a process by executable name (e.g. 'notepad.exe')."""
    if not process_name.lower().endswith(".exe"):
        process_name += ".exe"
    result = subprocess.run(
        ["taskkill", "/IM", process_name, "/F"],
        capture_output=True, text=True, shell=True
    )
    return (result.stdout + result.stderr).strip() or f"Closed {process_name}"


def list_running_processes() -> str:
    """List names of currently running processes."""
    result = subprocess.run(
        ["tasklist"], capture_output=True, text=True, shell=True
    )
    return result.stdout


def is_process_running(process_name: str) -> str:
    """Check whether a process with the given executable name is currently running."""
    result = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
        capture_output=True, text=True, shell=True
    )
    running = process_name.lower() in result.stdout.lower()
    return f"{process_name} is {'running' if running else 'not running'}."


# ---------------------------------------------------------------------------
# Mouse & keyboard
# ---------------------------------------------------------------------------

def mouse_click(x: int, y: int, button: str = "left") -> str:
    """Click the mouse at the given screen coordinates. Button can be 'left', 'right', or 'middle'."""
    pyautogui.click(x, y, button=button)
    return f"Clicked {button} at ({x}, {y})"


def mouse_double_click(x: int, y: int) -> str:
    """Double-click the mouse at the given screen coordinates."""
    pyautogui.doubleClick(x, y)
    return f"Double-clicked at ({x}, {y})"


def mouse_move(x: int, y: int) -> str:
    """Move the mouse to the given screen coordinates."""
    pyautogui.moveTo(x, y)
    return f"Moved mouse to ({x}, {y})"


def mouse_drag(x: int, y: int, to_x: int, to_y: int, duration: float = 0.5) -> str:
    """Drag the mouse from (x, y) to (to_x, to_y)."""
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(to_x, to_y, duration=duration)
    return f"Dragged from ({x}, {y}) to ({to_x}, {to_y})"


def mouse_scroll(clicks: int) -> str:
    """Scroll the mouse wheel. Positive clicks scroll up, negative scroll down."""
    pyautogui.scroll(clicks)
    direction = "up" if clicks > 0 else "down"
    return f"Scrolled {direction} {abs(clicks)} clicks"


def get_mouse_position() -> str:
    """Get the current mouse cursor position."""
    pos = pyautogui.position()
    return f"Mouse position: ({pos.x}, {pos.y})"


def keyboard_type(text: str) -> str:
    """Type text using the keyboard."""
    pyautogui.typewrite(text, interval=0.02)
    return f"Typed: {text}"


def keyboard_hotkey(keys: list[str]) -> str:
    """Press a keyboard shortcut. Pass keys as a list, e.g. ['ctrl', 'c'] for Ctrl+C."""
    pyautogui.hotkey(*keys)
    return f"Pressed: {'+'.join(keys)}"


def keyboard_press_key(key: str) -> str:
    """Press and release a single key (e.g. 'enter', 'esc', 'tab')."""
    pyautogui.press(key)
    return f"Pressed key: {key}"


def take_screenshot(filename: str = "screenshot.png") -> str:
    """Take a screenshot and save it to the workspace folder."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    path = os.path.join(WORKSPACE_DIR, filename)
    pyautogui.screenshot().save(path)
    return f"Screenshot saved to {path}"


# ---------------------------------------------------------------------------
# Clipboard
# ---------------------------------------------------------------------------

def get_clipboard_text() -> str:
    """Get the current text content of the clipboard."""
    return pyperclip.paste()


def set_clipboard_text(text: str) -> str:
    """Set the clipboard content to the given text."""
    pyperclip.copy(text)
    return f"Copied to clipboard: {text}"


# ---------------------------------------------------------------------------
# Filesystem
# ---------------------------------------------------------------------------

def list_directory(path: str = ".") -> str:
    """List files and folders inside the given directory path."""
    if not os.path.isdir(path):
        return f"'{path}' is not a valid directory."
    entries = os.listdir(path)
    return "\n".join(entries) if entries else "Directory is empty."


def create_folder(path: str) -> str:
    """Create a new folder at the given path (including any missing parent folders)."""
    os.makedirs(path, exist_ok=True)
    return f"Created folder: {path}"


def read_text_file(path: str) -> str:
    """Read and return the contents of a text file."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write_text_file(path: str, content: str) -> str:
    """Write (overwrite) text content to a file, creating parent folders if needed."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Wrote {len(content)} characters to {path}"


def copy_path(source: str, destination: str) -> str:
    """Copy a file or folder from source to destination."""
    if os.path.isdir(source):
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
        shutil.copy2(source, destination)
    return f"Copied '{source}' to '{destination}'"


def move_path(source: str, destination: str) -> str:
    """Move or rename a file or folder from source to destination."""
    shutil.move(source, destination)
    return f"Moved '{source}' to '{destination}'"


def delete_path(path: str) -> str:
    """Permanently delete a file or folder at the given path."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)
    return f"Deleted: {path}"


def search_files(directory: str, pattern: str) -> str:
    """Recursively search a directory for filenames containing `pattern` (case-insensitive)."""
    matches = []
    pattern = pattern.lower()
    for root, _, files in os.walk(directory):
        for name in files:
            if pattern in name.lower():
                matches.append(os.path.join(root, name))
    return "\n".join(matches) if matches else f"No files matching '{pattern}' found in '{directory}'."


# ---------------------------------------------------------------------------
# System / power / volume
# ---------------------------------------------------------------------------

def run_terminal_command(command: str) -> str:
    """Execute a shell command on Windows and return its stdout/stderr output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return (result.stdout + result.stderr).strip() or "Command executed with no output."


def open_url(url: str) -> str:
    """Open a URL in the default web browser."""
    webbrowser.open(url)
    return f"Opened {url} in default browser."


def lock_workstation() -> str:
    """Lock the Windows workstation (same as Win+L)."""
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    return "Workstation locked."


def set_system_volume(level_percent: int) -> str:
    """Set the system master volume to a percentage between 0 and 100."""
    if not _VOLUME_AVAILABLE:
        return "Volume control unavailable: pycaw/comtypes not installed."
    level_percent = max(0, min(100, level_percent))
    volume = AudioUtilities.GetSpeakers().EndpointVolume
    volume.SetMasterVolumeLevelScalar(level_percent / 100, None)
    return f"System volume set to {level_percent}%"


def mute_system_volume(mute: bool = True) -> str:
    """Mute or unmute the system master volume."""
    if not _VOLUME_AVAILABLE:
        return "Volume control unavailable: pycaw/comtypes not installed."
    volume = AudioUtilities.GetSpeakers().EndpointVolume
    volume.SetMute(1 if mute else 0, None)
    return "Muted system volume." if mute else "Unmuted system volume."


def shutdown_system(confirm: bool = False) -> str:
    """Shut down the Windows machine. Requires confirm=True to actually execute."""
    if not confirm:
        return "Shutdown not executed. Call again with confirm=True to proceed."
    subprocess.run(["shutdown", "/s", "/t", "0"])
    return "Shutting down..."


def restart_system(confirm: bool = False) -> str:
    """Restart the Windows machine. Requires confirm=True to actually execute."""
    if not confirm:
        return "Restart not executed. Call again with confirm=True to proceed."
    subprocess.run(["shutdown", "/r", "/t", "0"])
    return "Restarting..."


def sleep_system() -> str:
    """Put the Windows machine to sleep."""
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"])
    return "Going to sleep..."


def wait(seconds: int) -> str:
    """Wait for a specified number of seconds before continuing."""
    time.sleep(seconds)
    return f"Waited {seconds} seconds."


windows_toolkit = [
    # windows
    list_open_windows, activate_window, minimize_window, close_window, get_active_window_title,
    # applications
    open_application, close_application, list_running_processes, is_process_running,
    # mouse & keyboard
    mouse_click, mouse_double_click, mouse_move, mouse_drag, mouse_scroll, get_mouse_position,
    keyboard_type, keyboard_hotkey, keyboard_press_key, take_screenshot,
    # clipboard
    get_clipboard_text, set_clipboard_text,
    # filesystem
    list_directory, create_folder, read_text_file, write_text_file, copy_path, move_path,
    delete_path, search_files,
    # system
    run_terminal_command, open_url, lock_workstation, set_system_volume, mute_system_volume,
    shutdown_system, restart_system, sleep_system, wait,
]
