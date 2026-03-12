import webbrowser
from config import BROWSER_SHORTCUTS
from utils.logger import get_logger

logger = get_logger(__name__)


def try_open_browser(command: str) -> bool:
    """
    Check if the command matches a browser shortcut and open it.
    Returns True if handled, False otherwise.
    """
    for phrase, url in BROWSER_SHORTCUTS.items():
        if phrase in command.lower():
            logger.info(f"Opening {url}")
            webbrowser.open(url)
            return True
    return False
