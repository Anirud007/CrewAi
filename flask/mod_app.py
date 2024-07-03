from flask import Flask, render_template, url_for, redirect, jsonify, request

app = Flask(__name__)

crew_list = {}
agents = {}
crew_counter = 0
agent_counter = 0

# Frontend routers
@app.route('/')
def index():
    return render_template('mod_in.html')

@app.route('/page')
def mod_ind():
    crew_id = request.args.get('crew_id')
    return render_template('page.html', crew_id=crew_id)

@app.route('/page/<crew_id>/add_agent')
def add_agent(crew_id):
    return render_template('form_page.html', crew_id=crew_id)

# Crew endpoints
@app.route('/crews', methods = ['GET'])
def get_all_crew():
    return jsonify(crew_list)

@app.route('/crews/<crew_id>', methods=['GET'])
def get_crew(crew_id):
    crew_details = crew_list.get(crew_id)
    if crew_details is None:
        return jsonify({"Error": "Crew Not found"}), 404
    return jsonify(crew_details)
    
@app.route('/crews', methods = ['POST'])
def make_crew():
    global crew_counter
    if not request.is_json:
        return jsonify({"Error": "Invalid Input"}), 400
    try:
        content = request.get_json()

        crew_name = content.get('name')
        verbose = content.get('verbose')
        memorisation = content.get('memorisation')
        full_id = 'crew'+str(crew_counter)

        if bool(memorisation) == True:
            memorisation = True
        else:
            memorisation = False
        
        crew_list[full_id] = {
            "name" : crew_name,
            "verbose" : verbose,
            "memorisation": memorisation,
            "agents" : []
        }
        crew_counter += 1

    except Exception as e:
        return jsonify({"Error": f"{e}"}), 400
    return jsonify(crew_list[full_id]), 201

@app.route('/crews/<crew_id>', methods=['DELETE'])
def delete_instance(crew_id):
    if crew_id not in crew_list:
        return jsonify({"error": "Crew not found"}), 404
    
    del crew_list[crew_id]
    return jsonify({"message": "Crew deleted"}), 200

# Agents routes

@app.route('/crews/<crew_id>/agents', methods=['POST'])
def create_instance(crew_id):
    global agent_counter

    try:
        # content = request.get_json()
        if request.method == 'POST':

            role = request.form.get('name')
            backstory = request.form.get('backstory')
            goals = request.form.get('goals')
            task = request.form.get('task')
            tools = request.form.get('tools')
            exp_output = request.form.get('exp_output')
            allow_delegation = request.form.get('allow_delegation')
            
            # if bool(allow_delegation) != True:
            #     allow_delegation = False
            # else:
            #     allow_delegation = True

            full_id = 'agent'+ str(agent_counter)
            task_id = 'task' + str(agent_counter)

            # automater = Ai_Model(role, backstory, goal, task, exp_output, allow_delegation)
            # agent, tasks = automater.make_agent(full_id, task_id)
            
            # agent_list.append(agent)
            # task_list.append(tasks)
            # print(agent_list,'\n',task_list)

            # "exp_output": exp_output,
            # "allow_delegation" : allow_delegation

            agents[full_id] = {
                "id": full_id,
                "role": role,
                "backstory": backstory,
                "goals": goals,
                "task": task,
                "tools": tools
            }
            agent_counter+=1

            if crew_id not in crew_list:
                return jsonify({"Error" : "Crew Not Found"}) , 404
            crew_list[crew_id]["agents"].append(agents[full_id])
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

    return redirect(url_for('mod_ind'))
    
if __name__ == '__main__':
    app.run(debug=True)