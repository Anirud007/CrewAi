from flask import Flask, render_template, jsonify, request
# from flask_restful import Resource, Api
from crewai import Agent, Task, Crew



app = Flask(__name__)
# api = Api(app)

# agents = []

# class CrewAi:
#     def __init__(self, name, role, backstory, goal, tasks):
#         self.name = name
#         self.role = role
#         self.backstory = backstory
#         self.goal = goal
#         self.tasks = tasks

#     def perform_task(self):


@app.route('/create_agent', methods=['POST'])
def create_agent():
    data = request.get_json()
    agent_name = data['agent_name']
    goal = data['goal']
    backstory = data['backstory']
    task = data['task']
    tools = data['tools']

    agent = ca.Agent(name = agent_name, 
                     goal = goal, 
                     task = task, 
                     tools = tools
                )
    agent.add_task(task)
    for tool in tools:
        agent.add_tool(tool)

    return jsonify({'agent_id': agent.id})

if __name__ == '__main__':
    app.run(debug=True)