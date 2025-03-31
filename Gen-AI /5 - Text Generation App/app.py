from dotenv import load_dotenv # importing dotenv to load environment variables
import os 
from openai import AzureOpenAI # importing openai to use the GPT-3 API

# LEARNING 0 - Difference between accessing environment variables using dotenv and os
# "dotenv" is a package that loads environment variables from a .env file into os.environ without need of 
# explicitly setting them in the local system.
# "os.environ" is a dictionary that stores environment variables which are "already Set within the local system"

load_dotenv() # loading environment variables from our .evn file 

# Connecting to the Azure OpenAI API
client = AzureOpenAI(  
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),  
    api_key=os.getenv("OPENAI_API_KEY"),  
    api_version="2024-05-01-preview",
)

jokes_count = input("Enter the number of jokes you want to generate: ") # Taking input from the user

prompt = f"Generate {jokes_count} jokes about programmers." # Defining the prompt

# Providing the chat prompt
chat_prompt = [{
    "role": "user",
    "content" : prompt
  }]

# Defining the function that will generate text
completion = client.chat.completions.create(
  model=os.getenv("DEPLOYMENT_NAME"), # the model to use for completion
  messages=chat_prompt, # the prompt to complete
  max_tokens=800, # maximum number of tokens to generate
  temperature=1.0, # 0.0 is deterministic, 1.0 is maximum randomness
)

print(completion.choices[0].message.content) # printing the generated text


