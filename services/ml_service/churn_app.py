"""FastAPI-приложение для модели оттока."""
from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

from ml_service.churn_handler import FastApiHandler

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

main_app_predictions = Histogram(
    "main_app_predictions",
    "Histogram of predictions",
    buckets=[0.2, 0.4, 0.6, 0.8, 1.0]
)

main_app_counter = Counter(
    "main_app_counter",
    "Count of predictions"
)


@app.get("/")
def read_root() -> dict:
    """
    Root endpoint that returns the status of the service.

    Returns:
        dict: A dictionary indicating the service status.
    """
    return {"dr. Frankenstein": "It's alive"}


@app.post("/predict") 
def get_prediction_for_item(user_id: str, model_params: dict):
    """Функция для получения вероятности оттока пользователя, вероятность "target"==1

    Args:
        user_id (str): Идентификатор пользователя.
        model_params (dict): Параметры пользователя, которые нужно передать в модель.

    Returns:
        dict: Предсказание, на сколько вероятно, что пользователь уйдёт из сервиса.
    """
    all_params = {
        "user_id": user_id,
        "model_params": model_params
    }
    response = app.handler.handle(all_params)

    if set(response.keys()) == set(["user_id", "prediction"]):
        main_app_counter.inc()
        prediction = response["prediction"]
        main_app_predictions.observe(prediction)
    
    return response