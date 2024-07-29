Этап 1
  - Файл "Instructions.md" находится в mle-project-sprint-3-v001/services/ml_service
  
  Пример параметра для модели который отрабатывает без ошибок:
    {
        "paperless_billing": "No",
        "payment_method": "Bank transfer (automatic)",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "No",
        "streaming_movies": "No",
        "gender": "Male",
        "senior_citizen": 0,
        "partner": "Yes",
        "dependents": "Yes",
        "multiple_lines": "No",
        "monthly_charges": 21.0,
        "total_charges": 1493.75,
        "total_charges_sadsadas": 1493.75
    }
  
Этап 2
  - Для сбора, запуска и остановки контейнера нужны следующие команды. Команды запускаются из директории mle-project-sprint-3-v001/services

  docker image ls
  docker image build . -f Dockerfile_ml_service --tag churn_app:with_env
  docker image ls
  docker container run --publish 8081:8081 -d --env-file .env churn_app:with_env
  docker container ls
  docker container stop e8f9f4c19eff

Этап 3
  - для запуска docker compose нуждно запустить из директорий mle-project-sprint-3-v001/services команду:
  docker compose buld

  если уже все собрано но нужно только запустить контейнеры, то
  docker compose up

  - файл "prometheus.yml" находится в mle-project-sprint-3-v001/services/prometheus

  - /mle_projects/mle-project-sprint-3-v001/services$ docker container ls

    CONTAINER ID   IMAGE             COMMAND                  CREATED      STATUS             PORTS                                       NAMES
    c9bb1a36a01e   d4eea9e7c8b5      "/bin/sh -c 'uvicorn…"   2 days ago   Up About an hour   0.0.0.0:8081->8081/tcp, :::8081->8081/tcp   services-main-app-1
    3569809358d1   grafana/grafana   "/run.sh"                2 days ago   Up About an hour   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   services-grafana-1
    5028a338d02f   prom/prometheus   "/bin/prometheus --c…"   2 days ago   Up About an hour   0.0.0.0:9090->9090/tcp, :::9090->9090/tcp   services-prometheus-1

  соответственно у prometheus открыт порт 9090, у grafana порт 3000, у приложения порт 8081  

Этап 4
  - для запуска теста на нагрузку нуждно запустить из директорий mle-project-sprint-3-v001/services скрипт:
  python3.10 tests/load_test.py 3600 200 600 20 20
  данный скрипт с параметрами (3600, 200, 600, 20, 20) запустит нагрузку которая в среднем будет выдавать 60 запросов в секунду

  - файлы "dashboard.json", "dashboard.jpg", "Monitoring.md" находятся в директории mle-project-sprint-3-v001/services/grafana

