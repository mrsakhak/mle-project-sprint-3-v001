Наша задача сделать микросервис для предсказания стоимости недвижимости.

мы запустим микросервис несколькими спосабами 
     
     - командой из терминала
     
     - запустим docker контейнер
     
     - соберем и запустим docker compose

и последним этапом мы настроим мониторинг работающего микросервиса, запущенного через docker compose

Инструменты и библиотеки которые использовались
     
     - Visual Studio Code
     
     - FastAPI, uvicorn
     
     - Docker + Docker Compose
     
     - Prometheus + Grafana

Также для выполнения нашей задачи нам понадобится
     
     - предобученная модель, в которой уже есть препроцессинг
     
     - датасет квартир по которым мы можем делать предсказания (для имитации нагрузки)
     
     - скрипт который по датасету будет делать предсказания и нагружать микросервис
