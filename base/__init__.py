from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from base.utils import constant

SECRET_KEY = constant.secrets_key


def get_app() -> FastAPI:
    app = FastAPI()

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    return app
