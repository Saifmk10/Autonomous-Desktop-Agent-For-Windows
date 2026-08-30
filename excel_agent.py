from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
from langchain.agents  import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools


llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.1-pro-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

try : 
    server_params = StdioServerParameters(
            command="npx.cmd",
            args=["--yes", "@negokaz/excel-mcp-server"],
            )
    print(server_params)
    print("Server paramas added")
except Exception as error : 
    print("ERROR STARTING SERVER : " , error)

async def new():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()


            mcp_tools = await load_mcp_tools(session)

            # tool_selection = await session.list_tools()
            print("TOOLS ARE:" , mcp_tools)

            myagent = create_agent(
                model = llm,
                tools = mcp_tools
            )


            result = await myagent.ainvoke({
            "messages": [ 
                {
    "role": "user",
    "content": r"""Analyze and create a clean summary report for "D:\PROJECTS\LANGCHAIN_EXPLORATION\Autonomous-Desktop-Agent-For-Windows\INCOME DETAILS.xlsx":

1. Read: Inspect sheets and extract data from the active sheet.
2. Structure: Create an "Executive_Summary" sheet. Write structured KPI rows (Totals, Averages, Min/Max) using formulas like =SUM(...) and =AVERAGE(...). Do not use excel_create_table.
3. Style: Use excel_format_range to apply dark header fills, bold white text, cell borders, and currency number formats.
4. Verify: Take a screenshot using excel_screen_capture to confirm alignment."""
}
            ]
            })
            print(f"LLM RESPONSE: ----> \n", result["messages"][-1].content[0]["text"])

if __name__ == "__main__":
    asyncio.run(new())
