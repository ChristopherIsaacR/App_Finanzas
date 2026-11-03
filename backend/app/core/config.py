"""Configuración central. Lee variables de entorno (.env) con valores por defecto."""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]  # raíz del proyecto
DATA_DIR = BASE_DIR / "data"
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL") or f"sqlite:///{DATA_DIR / 'market.db'}"
    default_period: str = os.getenv("DEFAULT_PERIOD") or "5y"


settings = Settings()
