# MCP Learnings

This note explains the MCP flow used in this project in simple terms.

## Big Picture

Your code has 3 layers:

1. Launch configuration
2. Transport connection
3. MCP protocol session

Flow:

`StdioServerParameters -> stdio_client -> ClientSession -> list_tools/call_tool`

## 1) StdioServerParameters

`StdioServerParameters` is only a startup recipe.

In this project:

- `command="npx"`
- `args=["@playwright/mcp@latest"]`

That means: start the Playwright MCP server process using `npx @playwright/mcp@latest`.

Important:

- This object does not run tools.
- It only tells the client how to start the server process.

## 2) stdio_client(server_params)

`stdio_client(...)` uses the startup recipe and does two jobs:

1. Starts the MCP server subprocess.
2. Creates stdio pipes for communication.

When you write:

`async with stdio_client(server_params) as (read, write):`

- `read` is the incoming stream (server -> client).
- `write` is the outgoing stream (client -> server).

Important:

- `as` does not "pass data".
- `as` binds returned resources from the context manager to variables.

## 3) ClientSession(read, write)

`ClientSession` is the high-level MCP client API built on top of `read/write` streams.

When you write:

`async with ClientSession(read, write) as session:`

You can call methods like:

- `await session.initialize()`
- `await session.list_tools()`
- `await session.call_tool("browser_navigate", arguments={...})`

## Where do list_tools and call_tool come from?

These methods are from the MCP Python SDK (`ClientSession`), not from Playwright directly.

- `list_tools()` sends an MCP request: `tools/list`
- `call_tool(...)` sends an MCP request: `tools/call`

The server decides what tool names exist.

In your case, the Playwright MCP server exposes names like:

- `browser_navigate`
- `browser_snapshot`
- and others

## Why browser_navigate is not in Playwright docs

`browser_navigate` is an MCP tool name from the Playwright MCP server.

It is not a native Playwright Python/JS method name.

- Playwright library docs: browser automation API (`page.goto`, `page.click`, etc.)
- Playwright MCP docs: MCP tool names (`browser_navigate`, `browser_snapshot`, etc.)

## What creates the YAML files in .playwright-mcp?

The Playwright MCP server creates those artifacts when tools like `browser_snapshot` run.

Your code triggers it with:

`await session.call_tool("browser_snapshot", arguments={})`

So:

- Client requests snapshot.
- Server executes snapshot.
- Server writes YAML artifact.

## Practical Debug Rules

If you see `Connection closed` during `initialize()`:

1. Check `StdioServerParameters` command/args first.
2. Confirm the server command runs manually in terminal.
3. Then verify tool names from `list_tools()`.

If `call_tool` fails:

1. Ensure the tool name exists in `list_tools()` output.
2. Check argument schema/types.
3. Print full response content and errors.

## Corrected Mental Model

Your understanding, cleaned up:

- `StdioServerParameters` defines how to start the server process.
- `stdio_client` starts/connects and gives `read/write` streams.
- `ClientSession` uses those streams for MCP operations.
- `list_tools` and `call_tool` are client SDK methods.
- Actual tool implementations are on the server side.

This model is correct and enough for building real MCP clients.
