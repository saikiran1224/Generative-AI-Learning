# Our client should be able to interact with Math and Weather MCP servers 
from langchain_mcp_adapters.client import MultiServerMCPClient # This is a client that can interact with multiple MCP servers
from langgraph.prebuilt import create_react_agent # Helps to create an agent based on the input. 

from langchain_groq import ChatGroq # LLM 

from dotenv import load_dotenv
load_dotenv()

import asyncio 

async def main(): 

    # Creating the MCP Client 
    client = MultiServerMCPClient(
        {
            "math" : {
                "command" : "python",
                "args" : ["mathserver.py"], # Ensure correct Absolute Path of the file 
                "transport" : "stdio",
            },
            # "weather" : {
            #     "url" : "http://127.0.0.1:8000/mcp", # Ensure server is running 
            #     "transport" : "streamable-http",
            # }
        },  # type: ignore[arg-type]
    )

    tools = await client.get_tools()

    model = ChatGroq(model="qwen-qwq-32b")

    # Creating the agent 
    agent = create_react_agent(model, tools)

    # Invoking Math response
    math_response = await agent.ainvoke({
        "messages" : [{"role" : "user", "content" : "What is (3+5) * 12?"}]
    })

    print(math_response["messages"][-1].content)


# Calling the main function 
asyncio.run(main())




    



