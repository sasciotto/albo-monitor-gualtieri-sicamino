from __future__ import annotations

import os
from pathlib import Path


DEFAULT_BASE_URL = "https://comune.gualtieri.me.it/albo-pretorio"
DEFAULT_DB_PATH = "data/albo.sqlite"
DEFAULT_MAX_PAGES = 5
DEFAULT_DAYS = 7


def load_dotenv(path: str | Path = ".env") -> None:
    """Carica un file .env minimale senza dipendenze esterne.

    Le variabili già presenti nell'ambiente non vengono sovrascritte.
    """
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env_str(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def env_int(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Variabile {name} non valida: deve essere un numero intero")


def base_url() -> str:
    return env_str("ALBO_BASE_URL", DEFAULT_BASE_URL)


def db_path() -> str:
    return env_str("ALBO_DB", DEFAULT_DB_PATH)


def max_pages() -> int:
    return env_int("ALBO_MAX_PAGES", DEFAULT_MAX_PAGES)


def telegram_token() -> str:
    return env_str("ALBO_TELEGRAM_BOT_TOKEN")


def telegram_chat_id() -> str:
    return env_str("ALBO_TELEGRAM_CHAT_ID")
