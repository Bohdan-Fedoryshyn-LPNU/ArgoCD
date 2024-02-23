import requests
import time
import random

# Налаштування часових множників
TIME_SCALE = 100  # 1 секунда скрипта = 1000 секунд реального життя
DAY_SECONDS = 86400 // TIME_SCALE  # Кількість секунд у добі в масштабованому часі
WEEK_SECONDS = 7 * DAY_SECONDS  # Кількість секунд у тижні

def is_weekend(scaled_time):
    if scaled_time % WEEK_SECONDS >= 5 * DAY_SECONDS:
        print("Weekend")
        return 2
    print("Usual day")
    return 1

def is_nighttime(scaled_time):
    day_time = scaled_time % DAY_SECONDS
    if 9 * DAY_SECONDS // 24 <= day_time < 17 * DAY_SECONDS // 24:
        print("Night")
        return 0.5
    print("Day")
    return 1

def get_sleep_duration(scaled_time):
    cof = 1 * is_weekend(scaled_time) * is_nighttime(scaled_time)
    return random.uniform(0.01 * cof, 0.1 * cof) / TIME_SCALE
def send_request():
    try:
        requests.get("http://localhost:5000")
    except requests.exceptions.ConnectionError:
        pass  # Ignore connection errors for this simulation

def simulate_traffic():
    scaled_time = 0
    while True:
        send_request()
        time.sleep(get_sleep_duration(scaled_time))
        scaled_time += 1
        print(scaled_time)

if __name__ == '__main__':
    simulate_traffic()
