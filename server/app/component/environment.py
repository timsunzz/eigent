import importlib.util
import os
from pathlib import Path
from fastapi import APIRouter, FastAPI
from dotenv import load_dotenv
import importlib
from typing import Any, overload
from utils import traceroot_wrapper as traceroot

logger = traceroot.get_logger("environment")

logger.info("Loading environment variables from .env file")
load_dotenv()
logger.info("Environment variables loaded successfully")


@overload
def env(key: str) -> str | None: ...


@overload
def env(key: str, default: str) -> str: ...


@overload
def env(key: str, default: Any) -> Any: ...


def env(key: str, default=None):
    value = os.getenv(key)
    if value is None and key.upper() != key:
        value = os.getenv(key.upper())
    if value is None and key.lower() != key:
        value = os.getenv(key.lower())
    if value is None:
        value = default
    logger.debug("Environment variable accessed", extra={"key": key, "has_value": value is not None, "using_default": value == default})
    return value


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://") :]
    return url


def env_or_fail(key: str):
    value = env(key)
    if value is None:
        logger.error("Required environment variable missing", extra={"key": key})
        raise Exception("can't get env config value.")
    logger.debug("Required environment variable retrieved", extra={"key": key})
    return value


def env_not_empty(key: str):
    value = env(key)
    if not value:
        logger.error("Environment variable is empty", extra={"key": key})
        raise Exception("env config value can't be empty.")
    logger.debug("Non-empty environment variable retrieved", extra={"key": key})
    return value


def base_path():
    return Path(__file__).parent.parent.parent


def to_path(path: str):
    return base_path() / path


def auto_import(package: str):
    """
    自动导入指定目录下的全部py文件
    """
    # 获取文件夹下的所有文件名
    folder = package.replace(".", "/")
    files = os.listdir(folder)

    # 导入文件夹下的所有.py文件
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]  # 去掉文件名的扩展名.py
            importlib.import_module(package + "." + module_name)


def router_prefixes(configured: str | None) -> list[str]:
    """Serve both unprefixed and /api routes so Docker healthchecks and the desktop client agree.

    Railway/Docker probe GET /health. The Electron app always calls /api/*.
    """
    prefixes: list[str] = []
    for prefix in (configured or "", "", "/api"):
        if prefix not in prefixes:
            prefixes.append(prefix)
    return prefixes


def _load_controller_routers(directory: str) -> list[APIRouter]:
    dir_path = Path(directory).resolve()
    routers: list[APIRouter] = []

    for root, _, files in os.walk(dir_path):
        for file_name in files:
            if file_name.endswith("_controller.py") and not file_name.startswith("__"):
                file_path = Path(root) / file_name
                module_name = file_path.stem

                logger.debug("Processing controller file", extra={
                    "file_name": file_name,
                    "file_path": str(file_path)
                })

                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec is None or spec.loader is None:
                        logger.warning("Failed to create module spec", extra={"file_path": str(file_path)})
                        continue
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    router = getattr(module, "router", None)
                    if isinstance(router, APIRouter):
                        routers.append(router)
                        logger.debug("Router loaded successfully", extra={"module_name": module_name})
                    else:
                        logger.debug("No valid router found in module", extra={"module_name": module_name})

                except Exception as e:
                    logger.error("Failed to load controller module", extra={
                        "module_name": module_name,
                        "file_path": str(file_path),
                        "error": str(e)
                    }, exc_info=True)

    return routers


def auto_include_routers(api: FastAPI, prefix: str | list[str], directory: str):
    """
    自动扫描指定目录下的所有模块并注册路由

    :param api: FastAPI 实例
    :param prefix: 路由前缀，或一组前缀（同一套路由挂多次）
    :param directory: 要扫描的目录路径
    """
    prefixes = [prefix] if isinstance(prefix, str) else list(prefix)
    logger.info("Starting automatic router registration", extra={
        "prefix": prefixes,
        "directory": directory
    })

    routers = _load_controller_routers(directory)
    schema_prefix = "/api" if "/api" in prefixes else prefixes[0]

    for mounted in prefixes:
        for router in routers:
            api.include_router(
                router,
                prefix=mounted,
                include_in_schema=(mounted == schema_prefix),
            )

    logger.info("Automatic router registration completed", extra={
        "prefix": prefixes,
        "directory": directory,
        "routers_registered": len(routers)
    })
