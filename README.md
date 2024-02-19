# Сервис аутентификации

## Разворачивание проекта для разработки

- установка зависимостей
    - `poetry install`

- установка гит хуков
    - `pre-commit install`

- запуск проекта для разработки
    - перейти в scr `cd ./src`
    - запустить сервер `uvicorn main:app --reload`

- добавить секрет для токенов
    - `import secrets; secrets.token_hex()`

### Основные команды

- генерация миграций
    - `alembic revision --autogenerate -m "<название миграции>"`
- применение миграции
    - `alembic upgrade head`


### Запуск демо проекта

- перейти в директорию `cd ci/demo`
- запустить сборку docker-compose
    - `docker-compose -p auth-service-demo --env-file ./demo-db.env up`
