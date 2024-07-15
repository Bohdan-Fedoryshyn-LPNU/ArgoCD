import json
import yaml
import requests
import pandas as pd
from prophet import Prophet
import time
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Query Prometheus
current_time = int(time.time())
# Start time for 7 days (7 * 24 * 60 * 60 seconds) earlier
start_time = 1708092000
end_time = 1708109016
step = 15
period = 200

prometheus_url = 'http://localhost:9090/api/v1/query_range'
query = {'query': 'rate(flask_http_request_duration_seconds_bucket{le="0.75"}[5m])', 'start': start_time, 'end': end_time, 'step': step}
#response = requests.get(prometheus_url, params=query)
#data = response.json()

###  середнє значення
percent_of_limit_requests = 0.99 # 99%
percent_of_permissible_limit = 1.15 # 20%
global_average_threshold = 200

df = pd.read_csv('generated_data.csv')
interval_minutes = 5

periods=60* 1.25 * 60//interval_minutes
periods = int(periods)

def get_ARMA():

    # Train-test split
    train_size = int(len(df) - periods)
    train, test = df[:train_size], df[train_size:]

    # Fit ARIMA model
    order = (5, 1, 0)  # Example order, you may need to fine-tune this
    model = ARIMA(train['y'], order=order)
    fit_model = model.fit()

    # Forecast for the next 'periods' steps
    forecast = fit_model.forecast(steps=periods)

    print(forecast)

    return forecast

def alarm(cluster_name):
    print("ALARM!!!")

    # Завантажте вміст values.yaml
    with open('path/to/your/values.yaml', 'r') as file:
        values_data = yaml.safe_load(file)

    # Змініть параметр only_necessary
    values_data['only_necessary'] = True  # або False в залежності від вашого випадку

    # Запишіть змінений вміст назад у файл
    with open('path/to/your/values.yaml', 'w') as file:
        yaml.dump(values_data, file)

def check_status(cluster_name):
    forecast = get_ARMA()

    json_feature = json.loads(forecast.to_json(orient='records'))
    print(json_feature)

    print(len(json_feature))
    forecast_quantile = forecast.quantile(percent_of_limit_requests)
    print("forecast_quantile: ", forecast_quantile)

    if forecast_quantile > global_average_threshold * percent_of_permissible_limit:
            alarm()

while True:
    check_status()
    time.sleep(900)