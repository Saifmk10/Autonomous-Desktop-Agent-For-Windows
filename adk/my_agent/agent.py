from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StreamableHTTPConnectionParams
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv
from .windows_toolkit import windows_toolkit
load_dotenv()

# playwright mcp server
playwright = StdioServerParameters(
    command="npx",
    args=["@playwright/mcp@latest"],
)

# spotify is a remote MCP server (HTTP endpoint), not a local stdio process
spotify = StreamableHTTPConnectionParams(
    url="https://mcp-gateway-external-pilot.spotify.net/mcp",
)

windows = StdioServerParameters(
    command="uvx",
    args=["mcp-windows"],
)

# pincone mcp server
pinecone = StdioServerParameters(
    command="npx",
    args=[ "@pinecone-database/mcp"], 
    env={
        "PINECONE_API_KEY": os.environ["PINECONE_API_KEY"],
    },
)


root_agent = Agent(
    model='gemini-3.5-flash-lite',
    name='myAssistant',
    description='A helpful assistant for user questions.',
    instruction='''You are an autonomous AI agent with browser, vector-database, and Windows desktop-control tools. Use tools when they help complete the user's request.
                    After every interaction, store the user's message and your final response in the Pinecone `conversation` index for future context. Do this silently; never expose credentials or internal tool details.''',
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(server_params=playwright)
        ), 
        McpToolset(
            connection_params=StdioConnectionParams(server_params=pinecone)
        ),
        McpToolset(
            connection_params=spotify
        ),
        *windows_toolkit,
    ],
)
