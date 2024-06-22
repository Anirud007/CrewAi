from crewai import Agent, Task, Crew
# from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatCohere
import os
os.environ["COHERE_API_KEY"] = "TI0FhwlRBI7mRdPA3uAA5UeljckrQ9auiJshNRnZ"
llm = ChatCohere()
# llm = Ollama(model="llama2")

class Ai_Model:
    def __init__(self, name, backstory, goals, tools, task, exp_output):
        self.name = name
        self.backstory = backstory
        self.goals = goals
        self.tools = tools
        self.task = task
        self.exp_output = exp_output

    def make_agent(self, agent_name, agent_task):
        agent_name = Agent(role = self.name, 
                           goal = self.goals,
                           backstory = self.backstory,
                           llm = llm)
        
        agent_task = Task( description = self.task,
                          agent = agent_name,
                          expected_output = self.exp_output)
        
        return [agent_name, agent_task]
    
    # def make_crew(self , name_l, task_l):
    #     crew = Crew(agents=name_l,
    #                 tasks=task_l)
    #     return crew
    
    # def kickoff(self, crew):
    #     result = crew.kickoff() 
    #     return result

class make_crew:
    def m_crew(self, name_l, task_l):
        c = Crew(agents = name_l,
                 tasks = task_l)
        return c
    
    def run_crew(self, c):
        result = c.kickoff()
        return result

