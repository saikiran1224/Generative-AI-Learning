# End objective: To Learn LangChain by building a simple chat application using Prompt Templates and LLM (chat model) which translates text from English to a specified language.

# Step: 1 Import necessary libraries
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

# Step 2: Initialize the chat model
llm = init_chat_model(model="gemini-2.0-flash",model_provider="google_genai")

# Step 3: Define the prompt template which can be reused for different languages
prompt_template = ChatPromptTemplate(
    [
      ("system", "Translate the following from English into {language}."),
      ("user", "{text}") # user's input 
    ]
)

# Format the prompt using prompt_template.invoke({key: value}) method
filled_prompt = prompt_template.invoke({
    "language": "French",
    "text": "I love programming with Python!"
})

# Doing LLM call using invoke method on llm 
response = llm.invoke(filled_prompt)

print(response.content)




