"""FastAPI-приложение для модели оттока."""
from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

from ml_service.flats_handler import FastApiHandler

"""
Пример запуска:
uvicorn ml_service.app:app --reload --port 8081 --host 0.0.0.0

Для просмотра документации API и совершения тестовых запросов зайти на  http://127.0.0.1:8081/docs
"""

# создаём приложение FastAPI
app = FastAPI()
app.handler = FastApiHandler()

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

prom_request_counter = Counter('app_flats_request_counter', 'Count of request')
prom_error_counter = Counter('app_flats_error_counter', 'Count error responce')
prom_predictions = Histogram('app_flats_price_predictions', 'Histogram of flats price predictions',
    buckets=[i*(10**6) for i in range(30)]
)


@app.get("/")
def read_root() -> dict:
    """
    Root endpoint that returns the status of the service.

    Returns:
        dict: A dictionary indicating the service status.
    """
    return {'Staus': 'Ok'}


@app.post('/predict') 
def get_prediction_for_item(flat_id: str, model_params: dict):
    """Функция для получения вероятности оттока пользователя, вероятность "target"==1

    Args:
        flat_id (str): Идентификатор пользователя.
        model_params (dict): Параметры пользователя, которые нужно передать в модель.

    Returns:
        dict: Предсказание, на сколько вероятно, что пользователь уйдёт из сервиса.
    """
    prom_request_counter.inc()
    all_params = {
        'flat_id': flat_id,
        'model_params': model_params
    }
    response = app.handler.handle(all_params)
    
    if set(response.keys()) == set(['flat_id', 'prediction']):
        prediction = response['prediction']
        prom_predictions.observe(prediction)
    else:
        prom_error_counter.inc()
    
    return response