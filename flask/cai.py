from crewai import Agent, Task, Crew
# from langchain_community.llms import Ollama
from langchain_cohere import ChatCohere
# from langchain_community.chat_models import ChatCohere
import os
# os.environ['OPENAI_API_KEY'] = 'sk-proj-VeweXDbw16QP0pmlRYVhT3BlbkFJtKoXz641rIRYMtk4ZE9v'
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["COHERE_API_KEY"] = "TI0FhwlRBI7mRdPA3uAA5UeljckrQ9auiJshNRnZ"
# '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'
llm = ChatCohere()
# llm = Ollama(model="llama2")

class Ai_Model:
    def __init__(self, name, backstory, goals, task, exp_output, allow_delegation):
        self.name = name
        self.backstory = backstory
        self.goals = goals
        self.task = task
        self.exp_output = exp_output
        self.allow_delegation = allow_delegation

    def make_agent(self, agent_name, agent_task):
        agent_name = Agent(role = self.name, 
                           goal = self.goals,
                           backstory = self.backstory,
                           allow_delegation = self.allow_delegation,
                           verbose=True,
                           llm=llm)
        
        agent_task = Task( description = self.task,
                          agent = agent_name,
                          expected_output = self.exp_output)
        
        return [agent_name, agent_task]

class make_crew:
    def m_crew(self, name_l, task_l):
        c = Crew(agents = name_l,
                 tasks = task_l,
                 verbose = 1)
        return c
    
    def run_crew(self, c):
        result = c.kickoff()
        return result

