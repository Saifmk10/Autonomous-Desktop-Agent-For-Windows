import pyautogui
pyautogui.FAILSAFE = False

from langchain.tools import tool


@tool
def mouse_click(x: int, y: int, button: str = "left") -> str:
    """Click the mouse at the given screen coordinates. Button can be 'left', 'right', or 'middle'."""
    pyautogui.click(x, y, button=button)
    return f"Clicked {button} at ({x}, {y})"


@tool
def mouse_double_click(x: int, y: int) -> str:
    """Double-click the mouse at the given screen coordinates."""
    pyautogui.doubleClick(x, y)
    return f"Double-clicked at ({x}, {y})"


@tool
def mouse_move(x: int, y: int) -> str:
    """Move the mouse to the given screen coordinates."""
    pyautogui.moveTo(x, y)
    return f"Moved mouse to ({x}, {y})"


@tool
def mouse_drag(x: int, y: int, to_x: int, to_y: int, duration: float = 0.5) -> str:
    """Drag the mouse from (x, y) to (to_x, to_y)."""
    pyautogui.moveTo(x, y)
    pyautogui.dragTo(to_x, to_y, duration=duration)
    return f"Dragged from ({x}, {y}) to ({to_x}, {to_y})"


@tool
def mouse_scroll(clicks: int, x: int = None, y: int = None) -> str:
    """Scroll the mouse wheel. Positive clicks scroll up, negative scroll down."""
    pyautogui.scroll(clicks, x=x, y=y)
    direction = "up" if clicks > 0 else "down"
    return f"Scrolled {direction} {abs(clicks)} clicks"


@tool
def keyboard_type(text: str) -> str:
    """Type text using the keyboard."""
    pyautogui.typewrite(text, interval=0.02)
    return f"Typed: {text}"


@tool
def keyboard_hotkey(keys: list[str]) -> str:
    """Press a keyboard shortcut. Pass keys as a list, e.g. ['ctrl', 'c'] for Ctrl+C."""
    pyautogui.hotkey(*keys)
    return f"Pressed: {'+'.join(keys)}"


@tool
def screenshot() -> str:
    """Take a screenshot and save it to workspace/screenshot.png."""
    img = pyautogui.screenshot()
    img.save("./workspace/screenshot.png")
    return "Screenshot saved to workspace/screenshot.png"


@tool
def get_mouse_position() -> str:
    """Get the current mouse cursor position."""
    pos = pyautogui.position()
    return f"Mouse position: ({pos.x}, {pos.y})"


os_tools = [mouse_click, mouse_double_click, mouse_move, mouse_drag,
            mouse_scroll, keyboard_type, keyboard_hotkey, screenshot, get_mouse_position]
