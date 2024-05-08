from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import json
import flask_cors
import main  # Import your main.py

applcation = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
CORS(applcation, origins=['*'])

@applcation.route('/run-main', methods=['GET', 'POST'])
def run_main():
    data = request.json
    userPath = data["id"]
    print(userPath)
    # flash("You are successfully login into the Flask Application")
    # Assuming the data contains the necessary information
    # You can modify main.py to accept parameters as needed
    results = main.main(userPath)  # Execute the main function

    print(" AT FLASK RESULT: ")

    print(results)

    data = { 
            "status" : "success",
            "message" : "main.py executed",
        }
    
    result = jsonify(results)

    return jsonify(results)

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector

if __name__ == '__main__':
    applcation.run(debug=False, port=5000)


