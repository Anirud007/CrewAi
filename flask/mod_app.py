from flask import Flask, render_template, url_for, redirect, jsonify, request

app = Flask(__name__)

crew_list = {}
crew_counter = 0

@app.route('/')
def index():
    return render_template('mod_in.html')

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
        full_id = 'crew'+str(crew_counter)
        
        crew_list[full_id] = {
            "name" : crew_name
        }
        crew_counter += 1

    except Exception as e:
        return jsonify({"Error": f"{e}"}), 400
    return jsonify(crew_list[full_id]), 201
    
if __name__ == '__main__':
    app.run(debug=True)