from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET', "POST"])
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)