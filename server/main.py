import os
import sys
import pathlib

# Add project root to Python path to import shared utils
_project_root = pathlib.Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from utils import traceroot_wrapper as traceroot
from app import api
from app.component.environment import auto_include_routers, env, router_prefixes
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Only initialize traceroot if enabled
if traceroot.is_enabled():
    from traceroot.integrations.fastapi import connect_fastapi
    connect_fastapi(api)

logger = traceroot.get_logger("server_main")

prefix = env("url_prefix", "") or ""
auto_include_routers(api, router_prefixes(prefix), "app/controller")


@api.get("/api/docs", include_in_schema=False)
async def api_docs_alias():
    return RedirectResponse(url="/docs")


@api.get("/api/redoc", include_in_schema=False)
async def api_redoc_alias():
    return RedirectResponse(url="/redoc")


@api.get("/api/openapi.json", include_in_schema=False)
async def api_openapi_alias():
    return RedirectResponse(url="/openapi.json")
public_dir = os.environ.get("PUBLIC_DIR") or os.path.join(os.path.dirname(__file__), "app", "public")
if not os.path.isdir(public_dir):
    try:
        os.makedirs(public_dir, exist_ok=True)
        logger.warning(f"Public directory did not exist. Created: {public_dir}")
    except Exception as e:
        logger.error(f"Public directory missing and could not be created: {public_dir}. Error: {e}")
        public_dir = None

if public_dir and os.path.isdir(public_dir):
    api.mount("/public", StaticFiles(directory=public_dir), name="public")
else:
    logger.warning("Skipping /public mount because public directory is unavailable")
