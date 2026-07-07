

import asyncio

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

# this is the server param that needs to be provided to the mcp client so it can be accessable
server_params = StdioServerParameters( 
    command="npx",
    args=["@playwright/mcp@latest"],
)

#StdioServerParameters() >> defines how the server process needs to start 
#                     |
#                     |
#                     ---> stdio_client() >> starts the server and using the as passed the data into read and write  [config -> transport streams -> protocol session]
#                                      |
#                                      |
#                                      --->ClientSession() >> used to call various mcp fucntions such as list_tool() , call_tool() these tools are from the client sdk


# Optional: create a sampling callback
# async def handle_sampling_message(
#     context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
# ) -> types.CreateMessageResult:
#     print(f"Sampling request: {params.messages}")
#     return types.CreateMessageResult(
#         role="assistant",
#         content=types.TextContent(
#             type="text",
#             text="Hello, world! from model",
#         ),
#         model="gpt-3.5-turbo",
#         stopReason="endTurn",
#     )


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
            result = await session.call_tool("browser_navigate", arguments={"url": "https://www.saifmk.online"})
            for content in result.content:
                if isinstance(content, types.TextContent):
                    print(f"Navigate result: {content.text[:200]}")

            # Take a snapshot of the page
            print("\n--- Taking browser snapshot ---")
            snapshot = await session.call_tool("browser_snapshot", arguments={})
            for content in snapshot.content:
                if isinstance(content, types.TextContent):
                    print(f"Snapshot:\n{content.text[:500]}")

            # Keep the MCP session (and browser) alive until the user exits.
            await asyncio.to_thread(input, "\nPress Enter to close browser and exit... ")
            print("\nDone!")


def main():
    """Entry point for the client script."""
    asyncio.run(run())


if __name__ == "__main__":
    main()