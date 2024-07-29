"""Класс FastApiHandler, который обрабатывает запросы API."""
from catboost import CatBoostClassifier

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""
        
        # типы параметров запроса для проверки
        self.param_types = {
            "user_id": str,
            "model_params": dict
        }
        
        # список необходимых параметров модели и их порядок
        self.required_model_params = [
            'paperless_billing',
            'payment_method',
            'internet_service',
            'online_security',
            'online_backup',
            'device_protection',
            'tech_support',
            'streaming_tv',
            'streaming_movies',
            'gender',
            'senior_citizen',
            'partner',
            'dependents',
            'multiple_lines',
            'monthly_charges',
            'total_charges'
        ]
        
        model_path = "./models/catboost_model.cbm"
        self.load_model(model_path=model_path)
        
    def load_model(self, model_path: str):
        """Загружаем обученную модель предсказания кредитного рейтинга.
        
        Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostClassifier()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def model_predict(self, model_params: dict) -> float:
        """Выдает вероятность ухода клиента "target"==1.
        
        Args:
            model_params (dict): Параметры для модели.
        
        Returns:
            float — кредитный рейтинг
        """
        param_list = [model_params[param] for param in self.required_model_params]
        predict = self.model.predict_proba(param_list)[1]
        
        return predict
        
    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.
        
        Args:
            query_params (dict): Параметры запроса.
        
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if "user_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False

        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False

        return True

    
    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры для получения предсказаний.
        
        Args:
            model_params (dict): Параметры для получения предсказаний моделью.
        
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(self.required_model_params).issubset(set(model_params.keys())):
            return True
        else:
            return False
            

    def validate_params(self, params: dict) -> bool:
        """Проверяем корректность параметров запроса и параметров модели.
        
        Args:
            params (dict): Словарь параметров запроса.
        
        Returns:
             bool: True — если проверки пройдены, False — иначе
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
            
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        
        return True
                
                
    def handle(self, params):
        """Функция для обработки запросов API.
        
        Args:
            params (dict): Словарь параметров запроса.
        
        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # Валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                user_id = params["user_id"]
                model_params = params["model_params"]
                
                print(f"Predicting for user_id: {user_id} and model_params:\n{model_params}")
                
                prediction = self.model_predict(model_params)
                response = {
                    "user_id": user_id, 
                    "prediction": prediction
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response

