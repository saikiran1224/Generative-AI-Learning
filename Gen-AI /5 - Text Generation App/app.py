from dotenv import load_dotenv # importing dotenv to load environment variables
import os 
from openai import OpenAI # importing openai to use the GPT-3 API

# LEARNING 0 - Difference between accessing environment variables using dotenv and os
# "dotenv" is a package that loads environment variables from a .env file into os.environ without need of 
# explicitly setting them in the local system.
# "os.environ" is a dictionary that stores environment variables which are "already Set within the local system"

load_dotenv() # loading environment variables from our .evn file 


# Connecting to the Azure OpenAI API
client = OpenAI()

# Defining the function that will generate text
completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message)


