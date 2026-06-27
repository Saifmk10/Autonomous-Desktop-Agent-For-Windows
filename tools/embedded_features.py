import subprocess
import time

from langchain.tools import tool
from langchain_community.agent_toolkits import FileManagementToolkit
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("SERPER_API_KEY")

@tool
def run_terminal(command: str) -> str:
    """Execute terminal commands."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr


@tool
def wait(seconds: int) -> str:
    """Wait for a specified number of seconds before continuing."""
    time.sleep(seconds)
    return f"Waited {seconds} seconds."


@tool
def search_web(query: str) -> str:
    """Search the web for realtime information."""
    from langchain_community.utilities import GoogleSerperAPIWrapper

    search = GoogleSerperAPIWrapper(
        serper_api_key=key
    )
    result = search.run(query)
    return result


file_tools = FileManagementToolkit(root_dir="./workspace").get_tools()

system_tools = [run_terminal, wait, search_web] + file_tools
