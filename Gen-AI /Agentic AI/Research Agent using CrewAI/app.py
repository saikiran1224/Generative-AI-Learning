from crewai import Crew, Agent, Task, LLM # importing Crew, Agent, Task and Internal tool (LLMs)
from crewai_tools import SerperDevTool # importing External Tools - SerperAPI

from dotenv import load_dotenv # Environment variables
load_dotenv()

import os

topic = "Medical Industry" # User input for topic

# Creating LLM (Tool 1 - Configuring LLM)
llm = LLM(
    model="azure/gpt-4o", # call model by provider/model_name
    temperature=0.8, # 0.8 is default
    api_key=os.getenv('OPENAI_API_KEY'),
    api_base=os.getenv('AZURE_OPENAI_ENDPOINT')
)

# External/3rd Party Tool 2 (Serper API)
search_tool = SerperDevTool(n_results=3)

# Creating Agent 1 - Senior Research Analyst
# =============================================================================
senior_research_analyst = Agent(
    role = "Senior Research Analyst",
    goal = f"Research, analyse and synthesize comprehensive information on {topic} from reliable web sources.",
    backstory = '''
      You are a Senior Research Analyst at a leading AI research firm. Your goal is to research, analyse and synthesize comprehensive information on the topic of "Medical Industry using Generative AI" from reliable web sources. 
      You will be using the latest AI tools and technologies to assist you in your research. You will be working closely with your team to ensure that the 
      information you provide is accurate and up-to-date. Your research will be used to inform the development of new AI technologies in the medical industry.
    ''',
    allow_delegation = False, # allow the agent to delegate/modify other agents
    verbose = True, # show results in terminal 
    tools = [search_tool], # Assigning External Tools to Agent
    llm = llm # Assigning LLM to Agent
)

# Creating Task 1 - Task to be performed by Senior Research Analyst
# =============================================================================
research_task = Task(

    description = f'''
      1. Conduct comprehensive research on {topic} including: 
        - The current state of the medical industry
        - The role of AI in the medical industry
        - The impact of Generative AI on the medical industry
        - The challenges and opportunities in the medical industry
        - The future of AI in the medical industry 
      2. Analyse and synthesize the information gathered into a detailed report.
      3. Present the report to the team for further discussion and analysis.
      4. Provide recommendations on how AI can be leveraged in the medical industry.
      ''',
    
    expected_output = f'''
        A detailed report on the topic of "Medical Industry using Generative AI" including:
            - Overview of the current state of the medical industry
            - Analysis of the role of AI in the medical industry
            - Impact of Generative AI on the medical industry
            - Challenges and opportunities in the medical industry
            - Future of AI in the medical industry
            - Recommendations on leveraging AI in the medical industry
    ''',

    agent = senior_research_analyst
)


# Creating Agent 2 - Content Writer
# =============================================================================
content_writer = Agent(
    role = "Content Writer",
    goal = f"Write a detailed report on {topic} based on the research conducted by the Senior Research Analyst.",
    backstory = '''
      You are a Content Writer at a leading AI research firm. Your goal is to write a detailed report on the topic of "Medical Industry using Generative AI" based on the research conducted by the Senior Research Analyst. 
      You will be using the information provided by the Senior Research Analyst to create a comprehensive report that is accurate and informative. 
      Your report will be used to inform the development of new AI technologies in the medical industry.
    ''',
    allow_delegation = False, # allow the agent to delegate/modify other agents
    verbose = True, # show results in terminal 
    llm = llm # Assigning LLM to Agent
)

# Creating Task 2 - Task to be performed by Content Writer
# =============================================================================
writing_task = Task(

    description = f'''
      Write a detailed report on the topic of {topic} based on the research 
      conducted by the Senior Research Analyst.
      1. Transform technical information into an engaging and informative blog post.
      2. Maintain all factual accuracy and citations from the research.
      3. Preservers all source citations in [Source: URL] format.
      4. Follow proper markdown formatting guidelines.
    ''',

    expected_output = f'''
        A polished blog post in markdown format that:
         - Engages readers while maintaining a professional tone
         - Provides a detailed overview of the current state of the {topic}
         - Includes the inline citations hyperlinked to the original source URL.
         - Presents information in an accessible yet informative way
         - Follows proper markdown formatting guidelines, use H1 for the title and H3 for the sub-sections
    ''',

    agent = content_writer # Assigning Agent to Task
)

# Creating Crew
# =============================================================================

crew = Crew(
    name = "Research Crew",
    agents = [senior_research_analyst, content_writer], # Assigning Agents to Crew
    tasks = [research_task, writing_task], # Assigning Tasks to Crew
    verbose = True
)

result = crew.kickoff() # Starting the Crew

print(result) # Printing the result






