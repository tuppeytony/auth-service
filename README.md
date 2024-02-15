# Сервис аутентификации

## Рарворачивание проекта для разработки

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
