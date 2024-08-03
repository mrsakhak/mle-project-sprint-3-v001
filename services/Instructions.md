
Этап 1

    Для запуска сервиса нужно:

    из директории mle-project-sprint-3-v001/services создать виртуальное окружение
    
    >python3.10 -m venv .venv_deploy

    нужно войти в него и установить все что есть в "requirements.txt"
    
    >source .venv_deploy/bin/activate
    >pip install -r requirements.txt

    из директории mle-project-sprint-3-v001/services запустить сервис командой
    
    >uvicorn ml_service.flats_app:app --reload --port 8081 --host 0.0.0.0

    Можем зайти http://84.252.142.60:8081/docs (ip нужно заменить на свой) и проверить как отработает метод /predict

    Пример параметра для модели который отрабатывает без ошибок:
    {
        "building_type_int": 4,
        "has_elevator": true,
        "studio": false,
        "is_apartment": false,
        "total_area": 76.9000015258789,
        "build_year": 2012,
        "latitude": 55.71409606933594,
        "longitude": 37.40167236328125,
        "floor": 3,
        "kitchen_area": 12.699999809265137,
        "living_area": 46.20000076293945,
        "rooms": 3,
        "ceiling_height": 3.0,
        "flats_count": 147,
        "floors_total": 8,
        "floors_total_wqeqweqweqw": 8
    }
    
    Порядок параметров неважен. Параметры, которые  не участвуют в модели игнорируются.


Этап 2

    Все команды запускаются из директории mle-project-sprint-3-v001/services и не выходя из .venv_deploy
    Для сбора, запуска и остановки контейнера нужны следующие команды:

    Проверяем есть ли наш образ "flats_app" с тегом "with_env"
    
    >docker image ls
    
    Предположим его нет, тогда мы его создаем
    
    >docker image build . -f Dockerfile_ml_service --tag flats_app:with_env

    Проверяем есть ли наш образ "flats_app" тегом "with_env" - он должен появиться
    
    >docker image ls

    Проверяем запущен ли наш контейнер
    
    >docker container ls

    Предположим контейнер не запущен, тогда мы его запускаем
    
    >docker container run --publish 8081:8081 -d --env-file .env flats_app:with_env

    Проверяем запущен ли наш контейнер - должны его увидеть
    
    >docker container ls

    можем зайти http://84.252.142.60:8081/docs (ip нужно заменить на свой) и проверить как отработает метод /predict

    Остановим контейнер и удалим образ если есть в этом необходимость (container id - нужно заменить на свой)
    
    >docker container stop e8f9f4c19eff
    >docker image rm c16931ac78b8 -f

    Проверяем
    
    >docker container ls
    >docker image ls


Этап 3

    Для запуска docker compose нужно запустить из директорий mle-project-sprint-3-v001/services команду:
    
    >docker compose build

    если уже все собрано но нужно только запустить контейнеры, то нужна команда
    
    >docker compose up

    файл "prometheus.yml" находится в mle-project-sprint-3-v001/services/prometheus

    После запуска всех контейнеров из docker compose имеим доступ к сервисам через <ip>:<порт>
    
    >docker container ls

    CONTAINER ID   IMAGE               COMMAND                  CREATED         STATUS         PORTS                                       NAMES
    622a829be5a1   grafana/grafana     "/run.sh"                8 minutes ago   Up 8 minutes   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   services-grafana-1
    45db6991b0a3   services-main-app   "/bin/sh -c 'uvicorn…"   8 minutes ago   Up 8 minutes   0.0.0.0:8081->8081/tcp, :::8081->8081/tcp   services-main-app-1
    9a33b14e09a9   prom/prometheus     "/bin/prometheus --c…"   8 minutes ago   Up 8 minutes   0.0.0.0:9090->9090/tcp, :::9090->9090/tcp   services-prometheus-1

    соответственно:
        prometheus - http://84.252.142.60:9090
        grafana - http://84.252.142.60:3000
        приложение - http://84.252.142.60:8081  


Этап 4

    Для запуска теста на нагрузку нужно открфть еще один терминал и запустить из директорий mle-project-sprint-3-v001/services скрипт:
    
    >python3.10 tests/load_test.py cont 0.1 3600 200 600 20 20
    
    Этот скрипт с параметрами ("cont", 0.1, 3600, 200, 600, 20', 20") запустит нагрузку которая:
        - проработает 1 час (3600 секунд)
        - в среднем будет выдавать 60 запросов в секунду (600*20'/200)
        - с долей ошибок 10% (0.1)
    
    Файлы "dashboard.json", "dashboard.jpg", "Monitoring.md" находятся в директории mle-project-sprint-3-v001/services/grafana
        - нужно в grafana - http://84.252.142.60:3000 - создать conection "prometheus" с url "http://prometheus:9090/"
        - после этого загрузить "dashboard.json" через "import"
        - выбрать ранее сделанный "conection" и создать дашбоард