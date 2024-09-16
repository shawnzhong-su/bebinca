from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from bebinca.exts import db, requests, logs
from bebinca.exts.logs import logger, stop_logger


def create_app():
    app = Starlette()

    register_errors(app)
    register_events(app)
    register_middlewares(app)
    register_routers(app)
    return app


def register_errors(app):

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        try:
            logger.exception(exc)
        except (Exception,):
            pass
        return JSONResponse(
            {'detail': 'Internal server error'},
            status_code=500
        )


def register_events(app):
    from bebinca.exts.db import db

    @app.on_event('startup')
    async def startup():
        await db.connect()

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()
        await requests.close_httpx()
        try:
            logs.stop_logger()
        except (Exception,):
            pass


def register_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        max_age=600,
    )


def register_routers(app):
    from bebinca.urls import chat_url, user_url
    app.router.mount('/chats', chat_url.chat_url)
    app.router.mount('/users', user_url.user_url)


app = create_app()
