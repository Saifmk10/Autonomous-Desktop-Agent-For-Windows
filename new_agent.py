import asyncio
import traceback

from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import os
import json
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.1-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

try : 
    server_params = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp@latest"],
            )
    print("Server has started")
except Exception as error : 
    print("ERROR STARTING SERVER : " , error)


global list_of_tools

# fucntion responsible for passing the tool details
async def mcp_servers():
    

    try:

        async with stdio_client(server_params) as (reader, writer): #opens the connection with the server 
            async with ClientSession(reader, writer) as session: # opens the connection for communication with the server using session
                await session.initialize() # sends a ping to the server keeping the server ready for incomiong communications
                list_of_tools = await load_mcp_tools(session)
                print("TOOLS FROM THE ADAPTER : ", list_of_tools)

                # list_of_tools.append(tools)

                print("FINAL LIST OF TOOLS : ",list_of_tools)


                working_agent = create_react_agent(
                        model = llm,
                        state_modifier = "You Are an expert in browsing web and web automation agent , you are given acess to various tools that you can use on order to help the user with various tasks",
                        tools=list_of_tools
                    )

                result = await working_agent.ainvoke(
                        {
                            "input": "I want to buy latest MacBook from any ecommerce website"
                        }
                    )
                
                print(result)
                return result
                # await asyncio.Event().wait()

    except Exception as error : 
        print("ERROR: " , error)
        traceback.print_exc()



def agent():

    # starting the mcp server
    playwright = asyncio.run(mcp_servers())

    working_agent = create_agent(
        model = llm,
        system_prompt = "You Are an expert in browsing web and web automation agent , you are given acess to various tools that you can use on order to help the user with various tasks",
        tools=playwright
    )

    result = working_agent.invoke(
        {
            "messages" : [
                {
                    "role" : "user", 
                    "content" : "i want to buy latest mac book from any ecommerce website"
                }
            ]
        }
    )

    print(result)

    token_usage = result["messages"][-1]
    data =  token_usage.usage_metadata["output_tokens"]

    print("TOKEN USAGE:" , token_usage.usage_metadata["output_tokens"])

    with open("token_usage.json" , "w") as file:
        json.dump(data , file , indent=4)



if __name__ == "__main__":
    # agent() 
    asyncio.run(mcp_servers())
    # mcp_servers()