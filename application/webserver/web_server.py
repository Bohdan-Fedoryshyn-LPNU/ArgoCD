import random
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
import time
import math

app = Flask(__name__)
metrics = PrometheusMetrics(app)
request_counter = metrics.counter('webserver_requests', 'Request count by endpoints')
request_time = metrics.gauge('webserver_answer_time', 'Time for a request')
def cpu_intensive_task():
        # Calculating a large factorial
        math.factorial(random.randint(100000,500000))

@app.route('/')
@request_counter
def hello():
    start_time = time.time()
    # Емуляція обробки запиту
    cpu_intensive_task()
    # Збільшення лічильника запитів
    # Запис тривалості запиту
      # Increment the counter
    print(time.time() - start_time)
    return 'Hello World!'

if __name__ == '__main__':

    # Метрики Prometheus
    info = metrics.info('app_info', 'Application info', version='1.0.3')

    # Старт сервера для відображення метрик Prometheus
    # Старт Flask-сервера
    app.run(host='0.0.0.0', port=5000)
