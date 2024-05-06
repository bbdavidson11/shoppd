from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
import flask_cors
import main  # Import your main.py

app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
CORS(app, origins=['http://127.0.0.1:5500'])

@app.route('/run-main', methods=['GET', 'POST'])
@cross_origin(origin='http://127.0.0.1:5500')
def run_main():
    data = request.json
    # flash("You are successfully login into the Flask Application")
    # Assuming the data contains the necessary information
    # You can modify main.py to accept parameters as needed
    main.main()  # Execute the main function

    data = { 
            "status" : "success",
            "message" : "main.py executed",
        } 

    return jsonify({"status": "success", "message": "main.py executed"})

class Product:
    def __init__(self, image_url, image_vector):
        self.image_url = image_url
        self.image_vector = image_vector

if __name__ == '__main__':
    app.run(debug=True, port=5000)


