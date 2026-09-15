import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination


api = FastAPI(swagger_ui_parameters={"persistAuthorization": True})
add_pagination(api)

# Local Electron/web clients call this API from another origin. Without CORS,
# browser-based local mode (and some Electron fetch paths) fail silently.
_cors_origins = os.getenv("CORS_ORIGINS", "*")
_allow_origins = [origin.strip() for origin in _cors_origins.split(",") if origin.strip()]
# Browsers reject allow_origins=["*"] together with credentials.
_allow_credentials = _allow_origins != ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins,
    allow_credentials=_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
