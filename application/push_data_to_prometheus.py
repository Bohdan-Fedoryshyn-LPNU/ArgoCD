from flask import Flask, Response, request, jsonify
import json
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    # Read the JSON file
    with open('data/metrics.json', 'r') as file:
        data = json.load(file)

    # Convert data to Prometheus format
    prometheus_metrics = ""
    for entry in data:
        prometheus_metrics += f'{entry["metric"]} {entry["value"]}\n'

    return Response(prometheus_metrics, mimetype='text/plain')

@app.route('/save-file', methods=['POST'])
def save_file():
    # Check if a file is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Save the file in JSON format
        data_directory = 'data'
        os.makedirs(data_directory, exist_ok=True)
        file_path = os.path.join(data_directory, 'metrics.json')

        file_content = file.read()
        try:
            # Assuming the file content is a valid JSON string
            json_content = json.loads(file_content)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400

        with open(file_path, 'w') as json_file:
            json.dump(json_content, json_file)

        return jsonify({"message": "File saved successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
