from http.client import HTTPException
from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pwdlib import PasswordHash #для продакшена - argon2-cffi (или pwdlib, настроенный на Argon2).
from connect_db import SessionLocal
from models import User, Status, Genre, Genre_of_game, Game, Status_game_user
from auth import create_access_token, get_current_user
from datetime import date

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/games_arts", StaticFiles(directory="games_arts"), name="games_arts")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",
         summary="Главная страница",
         description="Страница входа и регистрации"
         )
def main_page(
        request: Request
):
    #for header1 in request.headers:
        #print(header1, ":", request.headers[header1])
    return templates.TemplateResponse(
        request = request,
        name = "main-page.html",
    )

@app.get("/listofgames",
         summary="Твой список игр",
         description="После успешной авторизации пользователь попадает сюда"
         )
def listofgames(
        request: Request,
        current_user: User = Depends(get_current_user),
        #user_id: int,
        db: SessionLocal = Depends(get_db)
):

    status = db.query(Status.status_title_ru).all()

    user = db.query(User).filter(User.id == current_user).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return templates.TemplateResponse(
        request = request,
        name = "list_of_games.html",
        context={
            "user_id": current_user,
            "username": user.username,
            "status_games": status
        }
    )

@app.post("/register",
          summary="Регистрация пользователя",
          description="Регистрация пользователя"
          )
def register(
        request: Request,
        nickname:str = Form(...),
        email:str = Form(...),
        password: str = Form(...),
        confirm_password: str = Form(...),
        db: SessionLocal = Depends(get_db),
):
    if password != confirm_password:
        return {"error": "Passwords don't match"}

    password_hash = PasswordHash.recommended()

    hashed = password_hash.hash(password)

    new_user = User(
        username=nickname,
        email=email,
        password=hashed,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # for head1 in request.headers:
    #     print(head1, ":", request.headers[head1])


    return RedirectResponse(
        url = f"/",
        status_code = 303,
    )

@app.post("/login",
          summary="Авторизация пользователя",
          description="Авторизация пользователя"
          )
def login_user(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: SessionLocal = Depends(get_db),
):
    user = db.query(User).filter(User.email==email).first()

    if not user:
        return {"error": "User not found"}

    password_hash = PasswordHash.recommended()

    is_correct = password_hash.verify(password, user.password)

    if not is_correct:
        return {"error": "Wrong password or email"}
    else:
        token = create_access_token(user.id)

        response = RedirectResponse(
            url = "/listofgames",
            status_code = 303
        )

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True
        )

        return response

@app.post("/addgame",
          summary="Добавить игру",
          description="Добавляет игру в общий список"
          )
def add_game(
    game_title: str = Form(...),
    #game_art: str,
    platform: str = Form(...),
    developer: str = Form(...),
    release_date: date = Form(...),
    db: SessionLocal = Depends(get_db),
):
    new_game = Game(
        game_title=game_title,
        platform=platform,
        developer=developer,
        release_date=release_date
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    # for head1 in request.headers:
    #     print(head1, ":", request.headers[head1])

    return RedirectResponse(
        url = "/listofgames",
        status_code = 303,
    )

@app.get("/logout",
         summary="Выход",
         description="Завершить сессию"
         )
def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response