from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import json
import flask_cors
import main
import firebase_admin
from firebase_admin import credentials, firestore, storage
import instantiate_firebase


applcation = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
CORS(applcation, origins=['*'])

@applcation.route('/run-main', methods=['GET', 'POST'])
def run_main():
    data = request.json
    userPath = data["id"]
    userShop = data["store"]

    print("firebase folder: " + userPath + ", store: " + userShop)
    # flash("You are successfully login into the Flask Application")
    # Assuming the data contains the necessary information
    # You can modify main.py to accept parameters as needed
    results = main.main(userPath, userShop)  # Execute the main function

    # print(" AT FLASK RESULT: ")
    # print(results)

    data = { 
            "status" : "success",
            "message" : "main.py executed",
        }
    
    result = jsonify(results)

    # we can also do render_template('output.html', data=jsonify(results)) - but we'll have to rewrite the js
    return jsonify(results)

if __name__ == '__main__':
    applcation.run(debug=False, port=5000)


