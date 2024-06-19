from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "crewai-llama2",
    base_url = "http://localhost:11434/v1")

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
    
    def make_crew(self , name_l, task_l):
        crew = Crew(agents=name_l,
                    tasks=task_l)
        return crew
    
    def kickoff(self, crew):
        result = crew.kickoff() 
        return result

