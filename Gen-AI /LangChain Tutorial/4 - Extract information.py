# End Objective: Extract information from text using LangChain and parse into a structured format

# Step 1: Loading Environment Variables and initialising chat model

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
llm = init_chat_model(model="gemini-2.0-flash",model_provider="google_genai")

# Step 2: Creating a pydantic object named `Person` and enabling llm to use structured output
from typing import Optional  # Importing library for optional typing
from pydantic import BaseModel, Field  # Importing library

class Person(BaseModel):
    """ Information about a person. """

    # Not forcing LLM to extract details even though its not present in the provided data

    name: Optional[str] = Field(default=None, description="The name of the person")
    hair_color: Optional[str] = Field(default=None, description="The color of the person's hair if known")
    height_in_meters: Optional[str] = Field(default=None, description="Height measured in feet")

class People(BaseModel):
    """ Information about multiple people. """

    people: list[Person] = Field(description="List of people with their details")

# Mentioning to LLM to use the structured output of the above Person object
structured_output_llm = llm.with_structured_output(People)

# Step 3: Creating a ChatpromptTemplate and giving the instructions to the LLM to extract information
from langchain.prompts import ChatPromptTemplate

extract_info_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in extracting information about people from text. You will extract the name, hair color, and height of each person mentioned in the text. If you do not know the value of an attribute asked to extract, return null for the attribute's value."),
        ("user", "{input}")
    ]
)

# Step 4: Invoking structured output llm with filled prompt
input_str = "Alice has brown hair and is 1.65 meters tall. Bob has blonde hair and is 1.80 meters tall. Charlie has no known hair color and is 1.75 meters tall."

updated_extract_info_prompt_template = extract_info_template.invoke({"input": input_str})

print(structured_output_llm.invoke(updated_extract_info_prompt_template))

