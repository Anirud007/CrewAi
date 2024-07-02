from flask import Flask, render_template, request, redirect, url_for
# from langchain_community.llms import Ollama
from cai import Ai_Model, make_crew
from langchain_community.chat_models import ChatCohere
import markdown
import os

os.environ["COHERE_API_KEY"] = "TI0FhwlRBI7mRdPA3uAA5UeljckrQ9auiJshNRnZ"

llm = ChatCohere()

# llm = Ollama(model="llama2")

app = Flask(__name__)

answer = ""
user_inputs = []
agent_list = []
task_list = []

@app.route('/')
def index():
    return render_template('index.html', user_inputs=user_inputs, answer=markdown.markdown(answer))

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
        
        automater = Ai_Model(name_input, backstory_input, goals_input, tools_input, task_input, "anything about the matter")
        agent, task = automater.make_agent(name_input, "task_name")
        
        agent_list.append(agent)
        task_list.append(task)

        return redirect(url_for('index'))
    
@app.route("/crew_agents", methods=['POST'])
def crew_agents():
    global answer
    if request.method == 'POST':
        crew = make_crew()
        ans = crew.m_crew(agent_list, task_list)
        answer = crew.run_crew(ans)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
