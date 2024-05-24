# Сервис аутентификации

## Разворачивание проекта для разработки

- установка зависимостей
  - `poetry install`

- установка гит хуков
  - `pre-commit install`

- запустить докер компоуз для локальной разработки
  - `docker-compose -p auth-service -f ./ci/local/docker-compose.yaml up -d`

- запуск проекта для разработки
  - перейти в scr `cd ./src`
  - запустить сервер `uvicorn main:app --reload`

- добавить секрет для токенов
  - `import secrets; secrets.token_hex()`

## Настройки vs code для локального дебага

Переходим в секцию run and debug и выбарем там create a launch.json file.
Перед началом нужно установить расширение python.
В окне выбираем python debugger и далее fastAPI. Выбираем в следующем окне main.py.
Пявятся конфиги для запуска дебага в виде json файла.

```json
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload"
            ],
            "jinja": true
        }
```

Этот json нужно дополнить этими 2 полями *justMyCode опциоланально можно добавить. для чего это нужно можно посмотреть в документации vs code*

```json
      "justMyCode": true,
      "cwd": "${workspaceFolder}/src"
```

В результате должно получится что то такое

```json
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true,
            "cwd": "${workspaceFolder}/src"
        }
```

И теперь можно через горячую клавишу F5 или в левой панели vs code выбрать run and debug
и там запустить с кнопки "play".
***
Есть еще вариант запуска дебага в vs code через докер конейнер. Перед этим обязательно установите в vscode расширение
docker.
Для этого нажимаем сочетание клавиш ctrl+shift+P. Откроется окно и в нем нужно выбрать
Docker: Initilize for docker debuging.
Далее выбираем python: fastAPI и указываем путь до main.py файла src/main.py.
В файле launch.json появится такой блок

```json
        {
            "name": "Docker: Python - Fastapi",
            "type": "docker",
            "request": "launch",
            "preLaunchTask": "docker-run: debug",
            "python": {
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}",
                        "remoteRoot": "/app"
                    }
                ],
                "projectType": "fastapi"
            }
        }
```

В текущем файле нужно поменять localRoot и remoteRoot на

```json
    "localRoot": "${workspaceFolder}/src",
    "remoteRoot": "/opt/app"
```

Далее нужно отредактировать файл tasks.json. Заменяем все в ключе tasks на это.

```json
[
  {
   "type": "docker-build",
   "label": "docker-build",
   "platform": "python",
   "dockerBuild": {
    "tag": "authservice:latest",
    "dockerfile": "${workspaceFolder}/ci/local/Dockerfile",
    "context": "${workspaceFolder}",
    "pull": true,
   }
  },
  {
   "type": "docker-run",
   "label": "docker-run: debug",
   "dependsOn": [
    "docker-build"
   ],
   "dockerRun": {
    "envFiles": ["./ci/local/.env"],
    "volumes": [{
     "containerPath": "/opt/app",
     "localPath": "./src"
    }],
    "network": "auth-service_default"
   },
   "python": {
    "args": [
     "main:app",
     "--host",
     "0.0.0.0",
     "--port",
     "8000",
     "--reload"
    ],
    "module": "uvicorn"
   }
  }
 ]
```

В зависимости от варианта работы нужно создать .env файлы для переменных окружения.
Пример для заполнения находится в `./ci/local/local.env.example`
Файл с созданными переменными окружения нужно положить в `./src/core` (в случае работы черех локальный дебаг) или
в `./ci/local` при работче через докер контейнер.
Для запуска тестов тоже нужно создать .env файл и положить его в `./tests/functional`. Пример переменных окружения лежит
`./tests/functional/.env.example`

### Основные команды

- генерация миграций
  - `alembic revision --autogenerate -m "<название миграции>"`
- применение миграции
  - `alembic upgrade head`
- проверка покрытия тестами
  - `dotenv -f src/core/.env run -- pytest --cov=src`
- проверка покрытия тестами c html отчетом
  - `dotenv -f src/core/.env run -- pytest --cov=src --cov-report=html`

### Запуск демо проекта

- запустить сборку docker-compose
  - `docker-compose -p auth-service-demo -f ./ci/demo/docker-compose.yaml --env-file ./ci/demo/demo-db.env up -d`

### Создание учетной записи для администратора

- Нужно добавить переменные окружения
  - `ADMIN_EMAIL` и `ADMIN_PASSWORD`
