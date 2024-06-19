from flask import Flask, render_template, request, redirect, url_for
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from cai import Ai_Model
import os
os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model = "crewai-llama2",
    base_url = "http://localhost:11434/v1")

app = Flask(__name__)

user_inputs = []

agent_list = []
task_list = []

@app.route('/')
def index():
    return render_template('index.html', user_inputs=user_inputs)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get name
        name_input = request.form['name']
        # Get backstory
        backstory_input = request.form['backstory']
        # get goals
        goals_input = request.form['goals']
        # Split the input by commas and strip any extra whitespace
        # input_goals = [item.strip() for item in goals_input.split(',')]
        # get Task
        task_input = request.form['task']
        # Get tools
        tools_input = request.form['tools']
         # Split the input by commas and strip any extra whitespace
        # input_tools = [item.strip() for item in tools_input.split(',')]
        # Store the inputs in the dictionary with the next index
        user_inputs.append({'name': name_input, 
                                   'backstory': backstory_input,
                                    'goals': goals_input,
                                    'task': task_input,
                                    'tools': tools_input})
        automater = Ai_Model(name_input, backstory_input,goals_input,tools_input,task_input, "anything about the matter")
        l = automater.make_agent(name_input, "task_name")
        agent_list.append(l[0])
        print(len(agent_list))
        task_list.append(l[1])
        print("Agent list is --> ", agent_list)
        print("task list is --> ", task_list)
        return redirect(url_for('index'))
    
@app.route("/crew_agents", methods=['GET', 'POST'])
def crew_agents():

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
