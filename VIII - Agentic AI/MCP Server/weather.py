from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather") # "Weather" is the name of the MCP server

@mcp.tool()
async def get_weather(location: str) -> str: 

    """ __summary__
    Get the weather for a given location 
    """
    # TODO: Implement the weather API call here 
    # For now, we'll just return a hardcoded response 

    return f"It's always raining in {location}"

# Run the MCP server 
if __name__ == "__main__":

    # Running using streamable-http transport protocol 
    # When we run this file using `python weather.py`, it will start the MCP server in the localhost:8000 or http:127.0.0.1:8000 and acts like our API endpoint and listen for incoming requests.
    # In realtime, we can usr our own API endpoint and setup the port accordingly.
    mcp.run(transport="streamable-http")
