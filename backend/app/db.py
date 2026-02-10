from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_KIOSK_DB_PATH = BASE_DIR / "database" / "kiosk.db"


def _get_env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key, default)
    if value is not None and value.strip() == "":
        return default
    return value


@lru_cache(maxsize=1)
def get_uni_engine() -> Engine:
    host = _get_env("UNI_DB_HOST", "127.0.0.1")
    port = _get_env("UNI_DB_PORT", "3306")
    name = _get_env("UNI_DB_NAME")
    user = _get_env("UNI_DB_USER")
    password = _get_env("UNI_DB_PASSWORD")

    if not all([name, user, password]):
        raise RuntimeError("UNI DB environment variables are not fully set")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_kiosk_engine() -> Engine:
    path = _get_env("KIOSK_DB_PATH", str(DEFAULT_KIOSK_DB_PATH))
    if not path:
        raise RuntimeError("KIOSK_DB_PATH is not set")

    return create_engine(
        f"sqlite:///{path}",
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
