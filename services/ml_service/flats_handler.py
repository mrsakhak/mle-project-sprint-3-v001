"""Класс FastApiHandler, который обрабатывает запросы API."""
import pickle
import pandas

class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""
        
        # типы параметров запроса для проверки
        self.param_types = {
            'flat_id': str,
            'model_params': dict
        }
        
        # загружаем модель и список необходимых параметров
        model_path = './models/flats/model.pkl'
        params_path = './models/flats/params.txt'
        self.load_model(
            model_path=model_path,
            params_path=params_path
        )


    def load_model(self, model_path: str, params_path: str):
        """Загружаем обученную модель предсказания кредитного рейтинга.
        
        Args:
            model_path (str): Путь до модели.
        """
        try:
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)
            with open(params_path, 'r') as params_file:
                params = params_file.read().splitlines()
                self.required_model_params = params
        except Exception as e:
            print(f'Failed to load model: {e}')


    def model_predict(self, model_params: dict) -> float:
        """Выдает предсказание стоимости квартиры.
        
        Args:
            model_params (dict): Параметры для модели.
        
        Returns:
            float — стоимость квартиры
        """
        params = dict()
        for key in model_params:
            params[key] = [model_params[key]]
        predict = self.model.predict(pandas.DataFrame(params))[0]
        return predict
        

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.
        
        Args:
            query_params (dict): Параметры запроса.
        
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if 'flat_id' not in query_params or 'model_params' not in query_params:
            return False
        elif not isinstance(query_params['flat_id'], self.param_types['flat_id']):
            return False
        elif not isinstance(query_params['model_params'], self.param_types['model_params']):
            return False
        else:
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
            print('All query params exist')
        else:
            print('Not all query params exist')
            return False
            
        if self.check_required_model_params(params['model_params']):
            print('All model params exist')
        else:
            print('Not all model params exist')
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
                print('Error while handling request')
                response = {'Error': 'Problem with parameters'}
            else:
                flat_id = params['flat_id']
                model_params = params['model_params']
                print(f'Predicting for flat_id: {flat_id} and model_params:\n{model_params}')
                prediction = self.model_predict(model_params)
                response = {
                    'flat_id': flat_id, 
                    'prediction': prediction
                }
        except Exception as e:
            print(f'Error while handling request: {e}')
            return {'Error': 'Problem with request'}
        else:
            return response

