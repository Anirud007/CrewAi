from crewai import Agent, Task, Crew, Process
# from langchain_community.llms import Ollama
from langchain_cohere import ChatCohere
import os
os.environ["COHERE_API_KEY"] = "TI0FhwlRBI7mRdPA3uAA5UeljckrQ9auiJshNRnZ"

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
        self.res = {}

    def callback_function(self, output):
        self.res[self.name] = f"{output.raw_output}"
        return self.res   

    def make_agent(self, agent_name, agent_task):
        agent_name = Agent(role = self.name, 
                           goal = self.goals,
                           backstory = self.backstory,
                           allow_delegation = self.allow_delegation,
                           verbose=True,
                           llm=llm)
        
        agent_task = Task(description = self.task,
                          agent = agent_name,
                          expected_output = self.exp_output,
                          callback = callback_function)
        
        return [agent_name, agent_task]

class make_crew:
    def m_crew(self, name_l, task_l):
        c = Crew(agents = name_l,
                 tasks = task_l,
                 process = Process.sequential)
        return c
    
    def run_crew(self, c):
        result = c.kickoff()
        return result

