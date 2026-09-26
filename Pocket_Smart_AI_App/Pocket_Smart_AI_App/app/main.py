from pathlib import Path

from fastapi import (
    FastAPI,
    Request
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates

from app.core.config import settings

from app.db.database import (
    Base,
    engine
)

from app.api.auth import (
    router as auth_router
)

from app.api.recommendations import (
    router as recommendation_router
)

import app.models


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(

    title=settings.app_name,

    version="1.0.0"
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.cors_list,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.mount(

    "/static",

    StaticFiles(
        directory=BASE_DIR / "static"
    ),

    name="static"
)


templates = Jinja2Templates(

    directory=BASE_DIR / "templates"
)


app.include_router(
    auth_router
)

app.include_router(
    recommendation_router
)


@app.get("/health")
def health():

    return {

        "status": "ok",

        "application":
            settings.app_name
    }


@app.get(
    "/",
    response_class=HTMLResponse
)
def index(request: Request):

    return templates.TemplateResponse(
        request,

        "index.html",

        {
            

            "title":
                "PocketSmart AI"
        }
    )


@app.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):

    return templates.TemplateResponse(
        request,

        "login.html",

        {
            
            

            "title":
                "Login"
        }
    )


@app.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(request: Request):

    return templates.TemplateResponse(
        request,

        "register.html",

        {
    
            

            "title":
                "Register"
        }
    )


@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_page(request: Request):

    return templates.TemplateResponse(
        request,

        "dashboard.html",

        {
            
            

            "title":
                "Dashboard"
        }
    )


@app.get(
    "/home",
    response_class=HTMLResponse
)
def home_page(request: Request):

    return templates.TemplateResponse(
        request,

        "home.html",

        {
            

            "title":
                "Home Planner"
        }
    )


@app.get(
    "/party",
    response_class=HTMLResponse
)
def party_page(request: Request):

    return templates.TemplateResponse(
        request,

        "party.html",

        {
            

            "title":
                "Party Planner"
        }
    )


@app.get(
    "/jewelry",
    response_class=HTMLResponse
)
def jewelry_page(request: Request):

    return templates.TemplateResponse(
        request,

        "jewelry.html",

        {
            

            "title":
                "Jewelry Planner"
        }
    )