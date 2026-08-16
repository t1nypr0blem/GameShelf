from sqlalchemy import create_engine, text #функция соединения с бд create_engine; text для сырых запросов
from sqlalchemy.orm import sessionmaker, declarative_base #declarative_base - все модели будут наследоваться от него
from dotenv import load_dotenv
import os

load_dotenv() #читает .env, находит ключ=значение и загружает в перем.окруж. ОС. Переменные попадают в os.environ["DATABASE_URL"]

DATABASE_URL = os.getenv("DATABASE_URL") #ищет DATABASE_URL в os.environ

engine = create_engine(DATABASE_URL) #создание поключения

SessionLocal = sessionmaker(bind=engine) #все будущие сессии должны использ. именно этот engine

Base = declarative_base() #база для всех моделей

#проверка соединения
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1")) #execute запускает команду к базе данных
    print(result.fetchone())