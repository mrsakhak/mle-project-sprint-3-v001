import sys
import requests
import random
import datetime
import time
import math

with open('datasets/flats_dataset.csv') as f:
    flats_rows = f.read().splitlines() 

def make_one_predict(error_prob=0.1):
    """Функция случайным образом берет строку из "datasets/flats_dataset.csv" и отправляет запрос на сервер
    
    Args:
        error_prob (float): вероятность отправки пустых параметров (имитация ошибки)

    Returns:
        response (response): Ответ от сервера
    """
    if random.random() < error_prob:
        model_params = dict()
    else:
        row_num = random.randrange(1, len(flats_rows))
        model_params = dict(zip(flats_rows[0].split(','), flats_rows[row_num].split(',')))
    
    response = requests.post('http://84.252.142.60:8081/predict?flat_id=0', json=model_params)
    return response

def make_several_predicts(error_prob=0.1, num=10):
    """Функция случайным образом берет строку из "datasets/flats_dataset.csv" и отправляет запрос на сервер
    
    Args:
        error_prob (float): вероятность отправки пустых параметров (имитация ошибки)
        num (int): Количество запросов к серверу 

    Returns:
        list of response (list): Массив ответов от сервера
    """
    return [make_one_predict(error_prob) for i in range(num)]

def make_continuous_predicts(error_prob=0.1, duration=20, period=5, dots_per_period=20, param_a=40, param_b=20):
    """Процедура для генерации переменной нагрузки согласно графику: y = a + b*sin(x)
    
    Args:
        error_prob (float): вероятность отправки пустых параметров (имитация ошибки)
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
        make_several_predicts(error_prob, predicts_count)
        
        whait_until_time = start_time + datetime.timedelta(seconds=step*step_num)
        delta_seconds_float = max(whait_until_time - datetime.datetime.now(), datetime.timedelta(0)).microseconds/1000000
        time.sleep(delta_seconds_float)

    print(f'Конец нагрузки:   {datetime.datetime.now()}')


params = dict()
match sys.argv[1]:
    case 'one':
        params['error_prob'] = float(sys.argv[2])
        print(make_one_predict(**params).content)
    case 'sev':
        params['error_prob'] = float(sys.argv[2])
        params['num'] = int(sys.argv[3])
        for response in make_several_predicts(**params):
            print(response.content)
    case 'cont':
        params['error_prob'] = float(sys.argv[2])
        params['duration'] = float(sys.argv[3])
        params['period'] = float(sys.argv[4])
        params['dots_per_period'] = int(sys.argv[5])
        params['param_a'] = float(sys.argv[6])
        params['param_b'] = float(sys.argv[7])
        make_continuous_predicts(**params)
        
