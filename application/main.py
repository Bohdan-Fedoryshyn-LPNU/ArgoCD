import json

import requests
import pandas as pd
from prophet import Prophet
import time
import matplotlib.pyplot as plt

# Query Prometheus
current_time = int(time.time())
# Start time for 7 days (7 * 24 * 60 * 60 seconds) earlier
start_time = 1708092000
end_time = 1708110290
step = 15
period = 200

prometheus_url = 'http://localhost:9090/api/v1/query_range'
query = {'query': 'rate(flask_http_request_duration_seconds_bucket{le="0.75"}[5m])', 'start': start_time, 'end': end_time, 'step': step}
response = requests.get(prometheus_url, params=query)
data = response.json()

###  середнє значення
percent_of_limit_requests = 0.99 # 99%
percent_of_permissible_limit = 1.15 # 20%



def alarm():
    pass

# # Convert data to DataFrame
# for item in data['data']['result']:
#     print(item)


timestamps = [point[0] for point in data['data']['result'][0]['values']]
values = [float(point[1]) for point in data['data']['result'][0]['values']]

timestamps = pd.to_datetime(timestamps, unit='s')


df = pd.DataFrame({'ds': timestamps, 'y': values})

model = Prophet()
model.fit(df)


future = model.make_future_dataframe(period, freq=str(step)+'s')  # Adjust the number of periods as needed
# Forecast
forecast = model.predict(future)
#forecast['yhat'] = forecast['yhat'].clip(lower=0)

# Plot forecast

model.plot(forecast)
model.plot_components(forecast)
print('--------------------------------------------')
json_feature = json.loads(forecast.to_json(orient='records'))
json_feature


print(len(json_feature))
part_of_period = 20
load_avarage = 0
loads = []
threshold = forecast['trend'].quantile(percent_of_limit_requests)
print("threshold: ", threshold)
global_average_threshold = forecast[forecast['trend'] > threshold]['trend'].mean()


for el in range(int(len(forecast)/part_of_period)):
    print(el)
    print(el*part_of_period)
    print((el+1)*part_of_period)
    part_of_forecast = forecast[el*part_of_period:(el+1)*part_of_period]
    threshold = part_of_forecast['trend'].quantile(percent_of_limit_requests)
    average_threshold = part_of_forecast[part_of_forecast['trend'] > threshold]['trend'].mean()
    print(average_threshold, " : ", global_average_threshold * percent_of_permissible_limit)
    if average_threshold > global_average_threshold * percent_of_permissible_limit:
        alarm()


# # Plotting the time series
# plt.figure(figsize=(100, 100))
# # plt.plot(df['ds'], df['y'])
# plt.plot(forecast['ds'], forecast['trend'])
# plt.xlabel('Timestamp')
# plt.ylabel('Request Count')
# plt.title('Request Count Over Time')
plt.show()