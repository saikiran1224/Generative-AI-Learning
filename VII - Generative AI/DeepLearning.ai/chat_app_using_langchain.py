from dotenv import load_dotenv
load_dotenv()
import os 

# Langchain imports
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

# Initialize the chat model
gemini_chat_model = init_chat_model(model="gemini-2.0-flash",model_provider="google_genai")

# Define the prompt
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that provides detailed and accurate responses to user queries in 5-7 lines."),
        ("human", "{user_input}")
    ]
)

# Creating chain by combining the chat model and the prompt
prompt_chain = chat_prompt_template | gemini_chat_model

# Creating a while loop which works until the user types 'exit'
while True: 

    # requesting user input 
    user_input = input("Please enter your query (type 'exit' to quit): ")

    if user_input.lower() == "exit":
        print("Exiting the chat application. Goodbye!")
        break

    # Generating the response using the prompt chain
    response = prompt_chain.invoke({
        "user_input": user_input
    })

    # Printing the response
    print(response.content)