# Importing FastMCP 
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Math") # "Math" is the name of the MCP server

# Creating first tool inside MCP Server
@mcp.tool()
def add(a: int, b: int) -> int: 
    """ __summary__
    Add two numbers together 
    """
    return a + b 

# Creating second tool inside MCP Server
@mcp.tool()
def multiply(a: int, b: int) -> int: 
    """ __summary__
    Multiply two numbers together 
    """
    return a * b 


if __name__ == "__main__": 

    # `transport = "stdio"` is the transport protocol for the MCP server.
    # It means it will use the standard input and output (stidin and stdout) to receive and respond to tool function calls.


    # If we run this file using `python mathserver.py`, it will start the MCP server but there will be no response, instead it will wait for input from the command prompt itself.
    # Since we are using`stdio`, user can interact with the MCP server by typing in the command prompt and provides the response back in the same command prompt itself.
    mcp.run(transport="stdio") # "stdio" is the transport protocol for the MCP server

