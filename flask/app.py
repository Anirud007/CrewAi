from flask import Flask, request, jsonify, render_template
from cai import Ai_Model, make_crew
import markdown
app = Flask(__name__)
print("hello")

# In-memory storage for instances
instances = {}
outputs = {}
agent_list = []
task_list = []

counter = 0

@app.route('/')
def index():
    return render_template('in.html')

# GET method to retrieve all instances
@app.route('/instances', methods=['GET'])
def get_all_instances():
    return jsonify(instances)


@app.route('/instances/<full_id>', methods=['GET'])
def get_instance(full_id):
    instance = instances.get(full_id)
    if instance is None:
        return jsonify({"error": "Instance not found"}), 404
    return jsonify(instance)


@app.route('/instances', methods=['POST'])
def create_instance():
    global counter
    if not request.is_json:
        return jsonify({"error": "Invalid input"}), 400

    try:
        content = request.get_json()

        role = content.get('role')
        backstory = content.get('backstory')
        goal = content.get('goal')
        task = content.get('task')
        exp_output = content.get('exp_output')
        allow_delegation = content.get('allow_delegation')
        
        if bool(allow_delegation) != True:
            allow_delegation = False
        else:
            allow_delegation = True

        full_id = 'agent'+ str(counter)
        task_id = 'task' + str(counter)

        automater = Ai_Model(role, backstory, goal, task, exp_output, allow_delegation)
        agent, tasks = automater.make_agent(full_id, task_id)
        
        agent_list.append(agent)
        task_list.append(tasks)
        print(agent_list,'\n',task_list)

        instances[full_id] = {
            "role": role,
            "backstory": backstory,
            "goal": goal,
            "task": task,
            "exp_output": exp_output,
            "allow_delegation" : allow_delegation
        }
        counter+=1
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

    return jsonify(instances[full_id]), 201

@app.route('/instances/<instance_id>', methods=['DELETE'])
def delete_instance(instance_id):
    if instance_id not in instances:
        return jsonify({"error": "Instance not found"}), 404
    
    agent_to_remove = None
    task_to_remove = None
    for agent in agent_list:
        if agent.role == instances[instance_id]['role']:
            agent_to_remove = agent
            break

    for task in task_list:
        if task.description == instances[instance_id]['task']:
            task_to_remove = task
            break

    if agent_to_remove:
        agent_list.remove(agent_to_remove)
    if task_to_remove:
        task_list.remove(task_to_remove)

    print(agent_list, '\n', task_list)
    
    del instances[instance_id]
    return jsonify({"message": "Instance deleted"}), 200

@app.route('/run_agents', methods=['POST', 'GET'])
def run_agents():
    crew = make_crew()
    cr = crew.m_crew(agent_list, task_list)
    output = crew.run_crew(cr)
    outputs['output'] = output
    return jsonify(output)

@app.route('/outputs', methods=['GET'])
def get_output():
    if outputs['output'] is None:
        return jsonify({"error": "no output"}), 404
    return jsonify(markdown.markdown(outputs['output']))

if __name__ == '__main__':
    app.run(debug=True)
