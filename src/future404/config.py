"""Central settings, read from environment variables (or a .env file)."""

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional
    pass


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY") or None
    model: str = os.getenv("FUTURE404_MODEL", "claude-opus-5-5")
    random_seed: int = 404

    @property
    def ai_enabled(self) -> bool:
        return self.anthropic_api_key is not None


settings = Settings()
