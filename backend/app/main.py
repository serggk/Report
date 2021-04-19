from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app import views
from app.db import init_db
from app.config import settings

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI()

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter(prefix='/api')
api_router.include_router(views.user_router)
api_router.include_router(views.login_router)
api_router.include_router(views.report_router)
api_router.include_router(views.opco_router)

app.include_router(api_router)
