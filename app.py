from flask import Flask, request, jsonify
import old_main  # Import your main.py

app = Flask(__name__)

@app.route('/run-main', methods=['POST'])
def run_main():
    data = request.json
    # Assuming the data contains the necessary information
    # You can modify main.py to accept parameters as needed
    old_main.main()  # Execute the main function
    return jsonify({"status": "success", "message": "main.py executed"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
