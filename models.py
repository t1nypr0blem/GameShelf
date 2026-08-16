from click import DateTime

from connect_db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Date, ForeignKey, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    game_title = Column(String, nullable=False, unique=True)
    game_art = Column(String)
    platform = Column(String)
    developer = Column(String)
    release_date = Column(Date)


class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    genre_name = Column(String, nullable=False)

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    status_title = Column(String)
    status_title_ru = Column(String)

class Genre_of_game(Base):
    __tablename__ = "genres_of_games"
    id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    genre = relationship("Genre")
    game = relationship("Game")

class Status_game_user(Base):
    __tablename__ = "status_game_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id")) #foreign_key="users.id")
    game_id = Column(Integer, ForeignKey("games.id"))
    game_status = Column(Integer, ForeignKey("status.id"))
    game_time_minute = Column(Integer) #количество минут за игрой (преобразовывать в часы)
    grade = Column(Integer) #оценка 0-10
    review = Column(String)
    replay = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user = relationship("User")
    game = relationship("Game")
    status = relationship("Status")

