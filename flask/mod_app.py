from flask import Flask, render_template, url_for, redirect, jsonify, request
from cai import Ai_Model, Makecrew
import markdown

app = Flask(__name__)

crew_list = {}
agents = {}

f_list = {}
outputs = {}

crew_counter = 0
agent_counter = 0

# Frontend endpoints
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

@app.route("/crews/<crew_id>/showoutput", methods=['GET', 'POST'])
def show_results(crew_id):
    return render_template("output.html", output = outputs )

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
        full_id = 'crew' + str(crew_counter)

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
    global f_list
    try:
        if request.method == 'POST':

            role = request.form.get('name')
            backstory = request.form.get('backstory')
            goals = request.form.get('goals')
            task = request.form.get('task')
            tools = request.form.get('tools')
            exp_output = request.form.get('exp_output')
            allow_delegation = request.form.get('allow_delegation')
            
            if bool(allow_delegation) != True:
                allow_delegation = False
            else:
                allow_delegation = True

            if bool(tools) != True:
                tools = False
            else:
                tools = True

            full_id = 'agent'+ str(agent_counter)
            task_id = 'task' + str(agent_counter)

            automater = Ai_Model(role, backstory, goals, task, exp_output, allow_delegation, outputs)
            agent, tasks = automater.make_agent(full_id, task_id)
            
            if crew_id not in f_list:
                f_list[crew_id] = {
                    "crew_agents" : [agent],
                    "crew_tasks" : [tasks]
                }
            else:
                f_list[crew_id]["crew_agents"].append(agent)
                f_list[crew_id]["crew_tasks"].append(tasks)

            print("\n\n\n", f_list, "\n\n\n")
            print("\n\n\n",f_list[crew_id]["crew_agents"],"\n\n\n")

            agents[full_id] = {
                "id": full_id,
                "role": role,
                "backstory": backstory,
                "goals": goals,
                "task": task,
                "exp_output": exp_output,
                "tools": tools,
                "allow_delegation" : allow_delegation
            }
            agent_counter+=1

            if str(crew_id) not in crew_list:
                return jsonify({"Error" : "Crew Not Found"}) , 404
            crew_list[crew_id]["agents"].append(agents[full_id])
    except Exception as e:
        return jsonify({"error" : f"{e}"}), 400

    return redirect(url_for('mod_ind'))


# output endpoint
# @app.route("/crews/<crew_id>/output", methods=['GET', 'POST'])
# def outputs(crew_id):
#     global outputs
#     global f_list
#     try:
#         crews = make_crew()
#         ans = crews.run_model(f_list[crew_id]["crew_agents"], f_list[crew_id]["crew_tasks"])
#         return jsonify(outputs)
#     except Exception as e:
#         return jsonify({"Error": f"{e}"}), 400
#     return jsonify({"Error" : "Cannot run Crew"})

@app.route("/crews/<crew_id>/output", methods=['GET', 'POST'])
def crew_output(crew_id):
    global outputs
    global f_list
    try:
        crews_instance = Makecrew(f_list[crew_id]["crew_agents"], f_list[crew_id]["crew_tasks"])  
        if crew_id not in f_list:
            return jsonify({"Error": "Crew Not Found"}), 404
        
        if len(f_list[crew_id]["crew_agents"]) != len(outputs):
            result = crews_instance.run_model()
            for i in outputs:
                outputs[i] = markdown.markdown(outputs[i])
        else:
            return redirect(url_for('show_results', crew_id=crew_id))
        
        return redirect(url_for('show_results', crew_id=crew_id))

    except Exception as e:
        return jsonify({"Error": str(e)}), 400
    
    return jsonify({"Error": "Cannot run Crew"})      
    
if __name__ == '__main__':
    app.run(debug=True)