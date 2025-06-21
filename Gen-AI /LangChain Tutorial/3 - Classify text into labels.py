# End Objective: Classify text into labels using LangChain  
# Tagging/Classify means Tagging means labeling a document with classes such as:
# - Sentiment
# - Language
# - Style (formal, informal etc.)
# - Covered topics
# - Political tendency

# Step 1: Load necessary libraries and Environment variables

from dotenv import load_dotenv
_ = load_dotenv()  # Load environment variables from .env file

from langchain.chat_models import init_chat_model
llm = init_chat_model(model="gemini-2.0-flash",model_provider="google_genai")


# Step 2: Creating a pydantic object named `Classification` and enabling llm to use structured output

from pydantic import BaseModel, Field # Importing library

class Classification(BaseModel):

    sentiment: str = Field(description="Sentiment of the text, e.g., positive, negative, neutral.")
    aggressiveness: int = Field(description="Aggressiveness level of the text, on a scale from 1 to 10.")
    language: str = Field(description="Language of the text, e.g., English, French, Spanish.")

# Mentioning to LLM to use the structured output of the above Classification object
structured_output_llm = llm.with_structured_output(Classification)

# Step 3: Creating a ChatpromptTemplate and giving the instructions to the LLM to classify the text

from langchain.prompts import ChatPromptTemplate

tagging_template = ChatPromptTemplate.from_template("""
                                                    
    Extract the desired information from the following passage.

    Only extract the properties mentioned in the 'Classification' function. 

    Passage:
    {input}  """)

# Step 4: Invoking strucuted output llm with filled prompt 

input_str = "Estoy increiblemente contento de haberte conocido! Creo que seremos muy buenos amigos!"

updated_tagging_prompt_template = tagging_template.invoke({"input": input_str})

print(structured_output_llm.invoke(updated_tagging_prompt_template))

