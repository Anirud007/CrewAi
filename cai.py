from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from crewai_tools import PDFSearchTool, ScrapeWebsiteTool, SerperDevTool, EXASearchTool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os
# os.environ["COHERE_API_KEY"] = "TI0FhwlRBI7mRdPA3uAA5UeljckrQ9auiJshNRnZ"

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ['EXA_API_KEY'] = os.getenv('EXA_API_KEY')

llm = ChatOpenAI(
    openai_api_base = "https://api.groq.com/openai/v1",
    openai_api_key = os.environ['GROQ_API_KEY'],
    model_name = "llama3-8b-8192",
    temperature = 0.1,
    max_tokens = 1000,
)

class Ai_Model:
    def __init__(self, name, backstory, goals, task, exp_output, allow_delegation, res, tools, file=None):
        self.name = name
        self.backstory = backstory
        self.goals = goals
        self.task = task
        self.exp_output = exp_output
        self.allow_delegation = allow_delegation
        self.res = res
        self.tools = tools
        self.rag_tool = PDFSearchTool(pdf=file,
                                        config=dict(
                                            llm=dict(
                                                provider="groq", 
                                                config=dict(
                                                    model="llama3-8b-8192",
                                                    # temperature=0.5,
                                                    # top_p=1,
                                                    # stream=true,
                                                ),
                                            ),
                                            embedder=dict(
                                                provider="huggingface", 
                                                config=dict(
                                                    model="BAAI/bge-small-en-v1.5",
                                                    # task_type="retrieval_document"
                                                    # title="Embeddings",
                                                ),
                                            ),
                                        )
                                    )
        self.serperdevsearch = SerperDevTool()
        self.scarpewebsite = ScrapeWebsiteTool()
        self.exasearchtool = EXASearchTool(k=5)
        self.tavilysearchresults = TavilySearchResults(k=5)
        

    def callback_function(self, output):
        self.res[self.name] = f"{output.raw_output}"
        return self.res   

    def make_agent(self, agent_name, agent_task):

        agent_name = Agent(role = self.name, 
                           goal = self.goals,
                           backstory = self.backstory,
                           allow_delegation = self.allow_delegation,
                           tools = self.tools,
                           verbose=True,
                           llm=llm)
        
        agent_task = Task(description = self.task,
                          agent = agent_name,
                          expected_output = self.exp_output,
                          callback = self.callback_function)
        
        return [agent_name, agent_task]

class Makecrew:
    def __init__(self, name_l, task_l, memory_status):
        self.name_l = name_l
        self.task_l = task_l
        self.memory_status = memory_status

    def run_model(self):
        c = Crew(agents = self.name_l,
                 tasks = self.task_l,
                 process = Process.sequential,
                 memory = self.memory_status,
                 embedder = dict(
                        provider="huggingface", 
                        config=dict(
                            model="BAAI/bge-small-en-v1.5",
                            # task_type="retrieval_document"
                            # title="Embeddings",
                            ),
                        ))

        result = c.kickoff()
        return result

