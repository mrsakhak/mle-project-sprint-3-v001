import sys
import requests
import random
import datetime
import time
import math

with open('datasets/churn_dataset.csv') as f:
    churn_rows = f.readlines()

def make_one_predict():
    """Функция случайным образом берет строку из "datasets/churn_dataset.csv" и отправляет запрос на сервер
    
    Args:
        None

    Returns:
        response (response): Ответ от сервера
    """
    row_num = random.randrange(1, len(churn_rows))
    model_params = dict(zip(churn_rows[0].split(','), churn_rows[row_num].split(',')))
    response = requests.post('http://84.252.142.60:8081/predict?user_id=0', json=model_params)
    return response

def make_several_predicts(num=10):
    """Функция случайным образом берет строку из "datasets/churn_dataset.csv" и отправляет запрос на сервер
    
    Args:
        num (int): Количество запросов к серверу 

    Returns:
        list of response (list): Массив ответов от сервера
    """
    return [make_one_predict() for i in range(num)]

def make_continuous_predicts(duration=20, period=5, dots_per_period=20, param_a=40, param_b=20):
    """Процедура для генерации переменной нагрузки согласно графику: y = a + b*sin(x)
    
    Args:
        duration (float): Длительность нагрузки в секундах.
        period (float): Длитенльность одного периода в секундах.
        dots_per_period (int): Количество моментов нагрузки в одном периоде.
        param_a (float): Параметр "a" в графике нагрузки.
        param_b (float): Параметр "b" в графике нагрузки.

    Returns:
        None
    """
    print(f'duration={duration}, period={period}, dots_per_period={dots_per_period}, param_a={param_a}, param_b={param_b}')

    step = period/dots_per_period
    duration_int = round(duration/step)

    print(f'Начало нагрузки:  {datetime.datetime.now()}')

    start_time = datetime.datetime.now()
    for step_num in range(duration_int):
        predicts_count = param_a + param_b*math.sin(2*math.pi*step_num/dots_per_period)
        predicts_count = round(predicts_count)
        make_several_predicts(predicts_count)
        
        whait_until_time = start_time + datetime.timedelta(seconds=step*step_num)
        delta_seconds_float = max(whait_until_time - datetime.datetime.now(), datetime.timedelta(0)).microseconds/1000000
        time.sleep(delta_seconds_float)

    print(f'Конец нагрузки:   {datetime.datetime.now()}')


params = dict()
match len(sys.argv):
    case 2:
        params['duration'] = float(sys.argv[1])
    case 4:
        params['duration'] = float(sys.argv[1])
        params['period'] = float(sys.argv[2])
        params['dots_per_period'] = int(sys.argv[3])
    case 6:
        params['duration'] = float(sys.argv[1])
        params['period'] = float(sys.argv[2])
        params['dots_per_period'] = int(sys.argv[3])
        params['param_a'] = float(sys.argv[4])
        params['param_b'] = float(sys.argv[5])
        
make_continuous_predicts(**params)

