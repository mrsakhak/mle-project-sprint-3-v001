Для запуска сервиса нужно:

из директории mle-project-sprint-3-v001/services создать виртуальное окружение
>python3.10 -m venv .venv_deploy

войти внего и установить все что есть в "requirements.txt"
>source .venv_deploy/bin/activate
>pip install -r requirements.txt

из директории mle-project-sprint-3-v001/services запустить сервис командой
>uvicorn ml_service.churn_app:app --reload --port 8081 --host 0.0.0.0