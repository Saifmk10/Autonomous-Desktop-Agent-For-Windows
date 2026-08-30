

import asyncio
from langchain.tools import tool
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

# this is the server param that needs to be provided to the mcp client so it can be accessable

@tool
def start_playwright_server():
    server_params = StdioServerParameters( 
        command="npx",
        args=["@playwright/mcp@latest"],
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection 
            await session.initialize()
            print("Session initialized successfully!")

            # List available tools
            tools = await session.list_tools()
            print(f"\nAvailable tools: {[t.name for t in tools.tools]}")

            # Call browser_navigate tool
            print("\n--- Navigating to example.com ---")
            result = await session.call_tool("browser_navigate", arguments={"url": "https://www.amazon.in/"})
            for content in result.content:
                if isinstance(content, types.TextContent):
                    print(f"Navigate result: {content.text[:200]}")

            # Take a snapshot to get element refs
            print("\n--- Taking browser snapshot ---")
            snapshot = await session.call_tool("browser_snapshot", arguments={})
            for content in snapshot.content:
                if isinstance(content, types.TextContent):
                    print(f"Snapshot:\n{content.text[:1000]}")

            # clicking on a button — use 'target' (not 'ref'), value comes from snapshot above
            # replace "e45" with the actual ref printed in the snapshot output
            print("\n--- clicking on a button ---")
            click = await session.call_tool("browser_click" , arguments={"element":"search box" , "target":"e90"})
            for content in click.content:
                if isinstance(content , types.TextContent):
                    print("ON CLICK : " , {content.text[:1000]})


            # searching for an item:
            print("\n ---- Searching for an item ----")
            search = await session.call_tool("browser_type" , arguments={"element":"Search Input" ,  "target":"e90" , "text":"mechanical keybaord"})
            search_item = await session.call_tool("browser_click" , arguments={"element":"search box" , "target":"e94"})




            # Keep the MCP session (and browser) alive until the user exits.
            await asyncio.to_thread(input, "\nPress Enter to close browser and exit... ")
            print("\nDone!")


def main():
    """Entry point for the client script."""
    asyncio.run(run())


if __name__ == "__main__":
    main()