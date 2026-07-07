# Autonomous Desktop Agent for Windows

An AI-powered agent that controls a Windows desktop end-to-end — launching applications, browsing the web, manipulating files, and interacting with the OS via natural language instructions.

## Features

- **Browser Automation** — Navigate, click, type, screenshot, and scrape via Playwright MCP
- **OS Control** — Mouse clicks, keyboard input, and window management via `pyautogui`/`pygetwindow`
- **Application Launcher** — Open and verify running desktop applications
- **File Management** — Read, write, and manage files through LangChain's `FileManagementToolkit`
- **Web Search** — Built-in search tool without opening a browser
- **Multi-LLM Support** — Works with Groq (Llama 3.3 70B) and Anthropic (Claude) backends

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph + LangChain |
| LLM backends | Groq, Anthropic Claude |
| Browser control | Playwright MCP (`@playwright/mcp`) |
| OS automation | pyautogui, pygetwindow |
| MCP client | `mcp` Python SDK |

## Project Structure

```
agent.py               # LangGraph agent with routing logic
anthropic_api.py       # Anthropic Claude client
mcp_testing.py         # MCP + Playwright session testing
tools/
  application_tools.py # Open and inspect desktop apps
  browser_tools.py     # Browser navigation and interaction
  embedded_features.py # File management and web search
  os_tools.py          # Mouse, keyboard, and OS-level control
```

## Getting Started

```bash
pip install -r requirments.txt
```

Set your API keys in a `.env` file:

```env
GORK_API_LLAMA_3_70B_VERSATILE=your_groq_key
ANTHROPIC_API_KEY=your_anthropic_key
```

Run the agent:

```bash
python agent.py
```

## License

MIT
