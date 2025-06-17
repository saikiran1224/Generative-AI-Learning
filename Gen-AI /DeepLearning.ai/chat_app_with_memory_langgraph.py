from dotenv import load_dotenv
load_dotenv()
import os 

# Langchain imports
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder # Import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage # Import AIMessage for full history

# Importing LangGraph components for state management and memory
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# Initialize the chat model
gemini_chat_model = init_chat_model(model="gemini-2.0-flash",model_provider="google_genai")

# Define the prompt template
# Use MessagesPlaceholder to inject the entire message history
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that remembers the user's name and provides detailed and accurate responses to user queries."),
        MessagesPlaceholder(variable_name="messages") # This will inject the list of BaseMessage objects
    ]
)

# Define a new graph - Langgraph StateGraph
workflow = StateGraph(state_schema=MessagesState)

# Defining a function to call the model
def call_model(state: MessagesState):
    # Pass the entire messages list to the prompt template
    prompt = chat_prompt_template.invoke({"messages": state["messages"]})
    
    # Generating the response using the chat model
    response = gemini_chat_model.invoke(prompt)
    
    # Return the response as an AIMessage within the messages list
    # LangGraph's MessagesState expects the return to be a dict with a "messages" key
    # that is a list of BaseMessage.
    return {"messages": [response]} # Wrap the response in a list

# Adding the edge from the START state to the model function
workflow.add_edge(START, "model")

# Adding the model (Single node) to the workflow
workflow.add_node("model", call_model)

# Adding a memory saver to the workflow
memory = MemorySaver()

# Compiling the workflow with the memory saver and checkpointing with the memory
app = workflow.compile(checkpointer=memory)

# Creating config for the app which helps when multiple users are using the app.
config = {"configurable": {"thread_id": "abc1234"}}

# --- Conversation 1 ---
print("--- Conversation 1 ---")
user_input_1 = "Hi, my name is Sai."
input_message_1 = [HumanMessage(content=user_input_1)]
output_response_1 = app.invoke({"messages": input_message_1}, config=config)
print("Turn 1 response:")
output_response_1["messages"][-1].pretty_print()

# --- Conversation 2 (using the same thread_id) ---
print("\n--- Conversation 2 ---")
user_input_2 = "What is my name?"
input_message_2 = [HumanMessage(content=user_input_2)]
# The 'config' ensures the same conversation thread is continued
output_response_2 = app.invoke({"messages": input_message_2}, config=config)
print("Turn 2 response:")
output_response_2["messages"][-1].pretty_print()

# --- Conversation 3 (another query to see continued memory) ---
print("\n--- Conversation 3 ---")
user_input_3 = "Can you tell me more about Large Language Models?"
input_message_3 = [HumanMessage(content=user_input_3)]
output_response_3 = app.invoke({"messages": input_message_3}, config=config)
print("Turn 3 response:")
output_response_3["messages"][-1].pretty_print()