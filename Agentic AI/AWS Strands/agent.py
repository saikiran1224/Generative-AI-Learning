# Environment variables     
import os 
from dotenv import load_dotenv
_ = load_dotenv() 

# Import necessary libraries
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import calculator, current_time, python_repl

model = LiteLLMModel(
    client_args={
        "api_key": os.getenv("GEMINI_API_KEY"),
    },
    model_id="gemini/gemini-2.0-flash",
    params={
        "temperature": 0.2,
    }
)

# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

# Create an agent with tools from the community-driven strands-tools package
# as well as our custom letter_counter tool
agent = Agent(tools=[calculator, current_time, python_repl, letter_counter], 
              model=model)

# Ask the agent a question that uses the available tools
message = """
I have 4 requests:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
4. Output a script that does what we just spoke about!
   Use your python tools to confirm that the script works before outputting it
"""

print(agent(message))
