from flask import Flask, render_template, jsonify, request
# from flask_restful import Resource, Api
from flask_cors import CORS
from crewai import Agent, Task, Crew

app = Flask(__name__)
CORS(app)
# api = Api(app)

# agents = []

class crwi:
    def __init__(self, name, role, backstory, goal, tasks):
        self.name = name
        self.role = role
        self.backstory = backstory
        self.goal = goal
        self.tasks = tasks

    def perform_task(self):
        results = []
        for task in self.tasks:
            result = f"{self.name} is performing task: {task['description']} using tools: {', '.join(task['tools'])}"
            results.append(result)
        return results
    
    def to_dict(self):
        return {
            "name": self.name,
            "backstory": self.backstory,
            "goal": self.goal,
            "tasks": self.tasks
        }

agents = []

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/api/agents', methods=['POST'])
def create_agent():
    data = request.json
    name = data.get('name')
    backstory = data.get('backstory')
    goals = data.get('goals', [])
    tasks = data.get('tasks', [])
    
    new_agent = crwi(name, backstory, goals, tasks)
    agents.append(new_agent)
    
    return jsonify({"status": "success", "agent_id": len(agents) - 1}), 201



if __name__ == '__main__':
    app.run(debug=True)