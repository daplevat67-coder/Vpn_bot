"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
DATA_DIR = BASE_DIR / "data"
MEDIA_DIR = BASE_DIR / "media"
BACKUPS_DIR = BASE_DIR / "backups"


@dataclass(frozen=True)
class Config:
    """Central configuration holder."""

    bot_token: str = ""
    admin_user_id: int = 0
    database_url: str = f"sqlite+aiosqlite:///{DATA_DIR / 'bot_builder.db'}"
    redis_url: str = "redis://localhost:6379/0"
    log_level: str = "INFO"
    backup_interval: str = "daily"
    max_bots_per_user: int = 10
    max_scenarios_per_bot: int = 50

    @classmethod
    def from_env(cls) -> Config:
        """Build config from environment variables."""
        return cls(
            bot_token=os.getenv("BOT_TOKEN", ""),
            admin_user_id=int(os.getenv("ADMIN_USER_ID", "0")),
            database_url=os.getenv("DATABASE_URL", cls.database_url),
            redis_url=os.getenv("REDIS_URL", cls.redis_url),
            log_level=os.getenv("LOG_LEVEL", cls.log_level),
            backup_interval=os.getenv("BACKUP_INTERVAL", cls.backup_interval),
            max_bots_per_user=int(os.getenv("MAX_BOTS_PER_USER", str(cls.max_bots_per_user))),
            max_scenarios_per_bot=int(os.getenv("MAX_SCENARIOS_PER_BOT", str(cls.max_scenarios_per_bot))),
        )


config = Config.from_env()
