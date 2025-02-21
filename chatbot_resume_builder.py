# Warning control
import warnings
warnings.filterwarnings('ignore')
import gradio as gr
import os
from crewai import Agent, Task, Crew
from crewai_tools import (
  FileReadTool,
  ScrapeWebsiteTool,
  MDXSearchTool,
  SerperDevTool
)
# from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import get_gemini_api_key, get_serper_api_key

# Set API keys
os.environ["GOOGLE_API_KEY"] = get_gemini_api_key()
os.environ["SERPER_API_KEY"] = get_serper_api_key()

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
read_resume = FileReadTool(file_path='./amit_resume.md')
semantic_search_resume = MDXSearchTool(mdx='./amit_resume.md')

# Define memory for agents
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Configure LLM
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.4,
    max_tokens=None,
    timeout=None,
    # max_retries=2
)

# Agent 1: Researcher
researcher = Agent(
    role="Tech Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job posting to help job applicants",
    tools = [scrape_tool, search_tool],
    verbose=True,
    backstory=(
        "As a Job Researcher, your prowess in "
        "navigating and extracting critical "
        "information from job postings is unmatched."
        "Your skills help pinpoint the necessary "
        "qualifications and skills sought "
        "by employers, forming the foundation for "
        "effective application tailoring."
    ),
    llm = gemini_llm
)

# Agent 2: Profiler
profiler = Agent(
    role="Personal Profiler for Engineers",
    goal="Do increditble research on job applicants "
         "to help them stand out in the job market",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Equipped with analytical prowess, you dissect "
        "and synthesize information "
        "from diverse sources to craft comprehensive "
        "personal and professional profiles, laying the "
        "groundwork for personalized resume enhancements."
    ),
    llm = gemini_llm
)

# Agent 3: Resume Strategist
resume_strategist = Agent(
    role="Resume Strategist for Engineers",
    goal="Find all the best ways to make a "
         "resume stand out in the job market.",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at refining resumes to highlight the most "
        "relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    ),
    llm = gemini_llm
)

# Agent 4: Interview Preparer
interview_preparer = Agent(
    role="Engineering Interview Preparer",
    goal="Create interview questions and talking points "
         "based on the resume and job requirements",
    tools = [scrape_tool, search_tool,
             read_resume, semantic_search_resume],
    verbose=True,
    backstory=(
        "Your role is crucial in anticipating the dynamics of "
        "interviews. With your ability to formulate key questions "
        "and talking points, you prepare candidates for success, "
        "ensuring they can confidently address all aspects of the "
        "job they are applying for."
    ),
    llm=gemini_llm
)

# Task for Researcher Agent: Extract Job Requirements
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences."
    ),
    agent=researcher,
    async_execution=True,
    output_file = 'resume_research.md'
)

# Task for Profiler Agent: Compile Comprehensive Profile
profile_task = Task(
    description=(
        "Compile a detailed personal and professional profile "
        "using the GitHub ({github_url}) URLs, and personal write-up "
        "({personal_writeup}). Utilize tools to extract and "
        "synthesize information from these sources."
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, "
        "project experiences, contributions, interests, and "
        "communication style."
    ),
    agent=profiler,
    async_execution=True,
    output_file = 'profile.md'
)

# Task for Resume Strategist Agent: Align Resume with Job Requirements
resume_strategy_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, tailor the resume to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "resume content. Make sure this is the best resume even but "
        "don't make up any information. Update every section, "
        "inlcuding the initial summary, work experience, skills, "
        "and education. All to better reflrect the candidates "
        "abilities and how it matches the job posting."
    ),
    expected_output=(
        "An updated resume that effectively highlights the candidate's "
        "qualifications and experiences relevant to the job."
    ),
    output_file="tailored_resume.md",
    context=[research_task, profile_task],
    agent=resume_strategist,
    
)

# Task for Interview Preparer Agent: Develop Interview Materials
interview_preparation_task = Task(
    description=(
        "Create a set of potential interview questions and talking "
        "points based on the tailored resume and job requirements. "
        "Utilize tools to generate relevant questions and discussion "
        "points. Make sure to use these question and talking points to "
        "help the candiadte highlight the main points of the resume "
        "and how it matches the job posting."
    ),
    expected_output=(
        "A document containing key questions and talking points "
        "that the candidate should prepare for the initial interview."
    ),
    output_file="interview_materials.md",
    context=[research_task, profile_task, resume_strategy_task],
    agent=interview_preparer,
)

job_application_crew = Crew(
    agents=[researcher,
            profiler,
            resume_strategist,
            interview_preparer],

    tasks=[research_task,
           profile_task,
           resume_strategy_task,
           interview_preparation_task],

    verbose=True,
)

job_application_inputs = {
    'job_posting_url': 'https://sandux.snaphunt.com/job/MFTH4LP0AU?source=linkedin',
    'github_url': 'https://github.com/AmitPratap175?tab=repositories',
    'personal_writeup': """ Amit Pratap is an accomplished Software
    Engineering Leader with 1 year 8 months of experience, specializing 
    in autonomous systems, sensor fusion, and AI-driven control. 
    At Rebhu Computing, he developed sensor calibration pipelines, 
    robust path-tracking algorithms, and AI-powered vehicle autonomy 
    solutions. He has designed state estimation models, neural 
    network-based vehicle controllers, and high-fidelity simulations 
    for drones and unmanned ground vehicles. His work spans drone 
    surveillance, AI-driven defect detection, and intelligent chatbots, 
    bridging AI and robotics for real-world impact.  
    Ideal for leadership roles that require a strategic and 
    innovative approach.""",
    "search_query": "Deep learning experience"
}
# {
#     'job_posting_url': 'https://jobs.lever.co/AIFund/6c82e23e-d954-4dd8-a734-c0c2c5ee00f1?lever-origin=applied&lever-source%5B%5D=AI+Fund',
#     'github_url': 'https://github.com/joaomdmoura',
#     'personal_writeup': """Noah is an accomplished Software
#     Engineering Leader with 18 years of experience, specializing in
#     managing remote and in-office teams, and expert in multiple
#     programming languages and frameworks. He holds an MBA and a strong
#     background in AI and data science. Noah has successfully led
#     major tech initiatives and startups, proving his ability to drive
#     innovation and growth in the tech industry. Ideal for leadership
#     roles that require a strategic and innovative approach.""",
#     "search_query": "Deep learning experience"
# }

# ### this execution will take a few minutes to run
# result = job_application_crew.kickoff(inputs=job_application_inputs)



def rhyme_chat2_stream(message, history, return_buffer=True):
    '''This is a generator function, where each call will yield the next entry'''

    # chat_gen = job_application_crew.kickoff(inputs=job_application_inputs)
    # return chat_gen

    for task in job_application_crew.tasks:
        result = task.execute()  # Run each task individually
        yield f"Task {task.description[:50]}... completed.\nResult:\n{result}\n"


## Simple way to initialize history for the ChatInterface
chatbot = gr.Chatbot(value = [[None, "Hi, how may I help?"]])

## IF USING COLAB: Share=False is faster
gr.ChatInterface(rhyme_chat2_stream, chatbot=chatbot).queue().launch(debug=True, share=True)