from flask import Flask, request

app = Flask(__name__)

@app.route('/alarm', methods=['GET', 'POST'])
def alarm():
    if request.method == 'POST':
        # Handle POST request
        data = request.json
        return "Alarm Received: " + str(data), 200
    else:
        # Handle GET request
        return "Alarm Service. Send a POST request with data.", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
