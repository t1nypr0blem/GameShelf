# GameShelf

## Стек:
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Jinja2
- HTML/CSS
- PyJWT
- Docker

Реализовано:
- Регистрация и авторизация
- Авторизация с использованием JWT access-токена
- Работа с PostgreSQL через SQLAlchemy
- Контейнеризация проекта с помощью Docker

Запуск:
1. В терминале: git clone [репозиторий]
2. Перейти в папку проекта (cd [папка проекта])
2. Создать .env на основе .env.example
3. В терминале: docker compose up --build
4. При успешном запуске проект будет доступен по адресу http://127.0.0.1:8000/, документация - http://127.0.0.1:8000/docs