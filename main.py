from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.post("/login", response_class=HTMLResponse)
async def login_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    if username not in users or users[username] != password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Wrong login or password!"
            }
        )

    return RedirectResponse(url=f"/profile?username={username}", status_code=302)

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@app.post("/register", response_class=HTMLResponse)
async def register_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    if username in users:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username already exists!"}
        )

    users[username] = password

    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    return templates.TemplateResponse(
        "register.html",
        {"request": request, "success": "Registration successful! Please login!"}
    )

@app.get("/profile", response_class=HTMLResponse)
async def profile_user(request: Request, username: str):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": username}
    )