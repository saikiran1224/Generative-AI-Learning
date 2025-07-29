from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from typing import Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import BaseMessage

from langchain_groq import ChatGroq

# Defining LLM
llm = ChatGroq(model="llama3-8b-8192")

# Defining State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def tool_agent_definition():

    # Defining tool - add function
    def add(a: int, b: int) -> int: 
        """ Add a and b 
        Args:
            a (int): first int
            b (int): second int 
        Returns: 
            int: output  
        """
        return a + b 
    
    tools = [add] # adding all the tools here

    # binding llm with tools
    llm_with_tools = llm.bind_tools(tools)

    # Node definitioon
    def tool_calling_llm(state: State):
        return { "messages" : [llm_with_tools.invoke(state["messages"])]}

    # Building graph
    builder = StateGraph(State)

    # Adding Nodes
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))

    # Adding Graphs
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools","tool_calling_llm")

    graph = builder.compile()

    return graph

tool_agent = tool_agent_definition()

response = tool_agent.invoke({"messages" : "Hello How are you?"})

print(response)





