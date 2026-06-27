import os
import webbrowser
from langchain.tools import tool


@tool
def browser_navigate(url: str) -> str:
    """Navigate the browser to a URL."""
    webbrowser.open(url)
    return f"Navigated to {url}"


@tool
def browser_click(selector: str) -> str:
    """Click an element on the page by CSS selector."""
    page = _get_page()
    page.click(selector)
    return f"Clicked: {selector}"


@tool
def browser_type(selector: str, text: str) -> str:
    """Type text into an input field identified by CSS selector."""
    page = _get_page()
    page.fill(selector, text)
    return f"Typed '{text}' into {selector}"


@tool
def browser_press_key(key: str) -> str:
    """Press a keyboard key in the browser (e.g. 'Enter', 'Tab', 'Escape')."""
    page = _get_page()
    page.keyboard.press(key)
    return f"Pressed key: {key}"


@tool
def browser_get_text(selector: str) -> str:
    """Get the text content of an element by CSS selector."""
    page = _get_page()
    element = page.locator(selector)
    return element.inner_text()


@tool
def browser_get_page_content() -> str:
    """Get the visible text content of the current page (truncated to 5000 chars)."""
    page = _get_page()
    content = page.inner_text("body")
    return content[:5000]


@tool
def browser_get_url() -> str:
    """Get the current page URL."""
    page = _get_page()
    return page.url


@tool
def browser_get_title() -> str:
    """Get the current page title."""
    page = _get_page()
    return page.title()


@tool
def browser_go_back() -> str:
    """Navigate back in browser history."""
    page = _get_page()
    page.go_back()
    return f"Navigated back. Now at: {page.url}"


@tool
def browser_go_forward() -> str:
    """Navigate forward in browser history."""
    page = _get_page()
    page.go_forward()
    return f"Navigated forward. Now at: {page.url}"


@tool
def browser_refresh() -> str:
    """Refresh the current page."""
    page = _get_page()
    page.reload()
    return f"Refreshed: {page.url}"


@tool
def browser_screenshot(path: str = "./workspace/browser_screenshot.png") -> str:
    """Take a screenshot of the current browser page."""
    page = _get_page()
    page.screenshot(path=path)
    return f"Screenshot saved to {path}"


@tool
def browser_scroll_down(pixels: int = 500) -> str:
    """Scroll down on the current page."""
    page = _get_page()
    page.evaluate(f"window.scrollBy(0, {pixels})")
    return f"Scrolled down {pixels}px"


@tool
def browser_scroll_up(pixels: int = 500) -> str:
    """Scroll up on the current page."""
    page = _get_page()
    page.evaluate(f"window.scrollBy(0, -{pixels})")
    return f"Scrolled up {pixels}px"


@tool
def browser_wait_for_selector(selector: str, timeout: int = 5000) -> str:
    """Wait for an element to appear on the page."""
    page = _get_page()
    page.wait_for_selector(selector, timeout=timeout)
    return f"Element found: {selector}"


@tool
def browser_select_option(selector: str, value: str) -> str:
    """Select an option from a dropdown by value."""
    page = _get_page()
    page.select_option(selector, value)
    return f"Selected '{value}' in {selector}"


@tool
def browser_hover(selector: str) -> str:
    """Hover over an element by CSS selector."""
    page = _get_page()
    page.hover(selector)
    return f"Hovered over: {selector}"


@tool
def browser_close() -> str:
    """Close the browser."""
    global _playwright, _context, _page
    if _context:
        _context.close()
        _context = None
        _page = None
    if _playwright:
        _playwright.stop()
        _playwright = None
    return "Browser closed."


browser_tools = [
    browser_navigate, browser_click, browser_type, browser_press_key,
    browser_get_text, browser_get_page_content, browser_get_url, browser_get_title,
    browser_go_back, browser_go_forward, browser_refresh, browser_screenshot,
    browser_scroll_down, browser_scroll_up, browser_wait_for_selector,
    browser_select_option, browser_hover, browser_close
]