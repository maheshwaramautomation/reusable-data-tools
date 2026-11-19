"""Small, dependency-free environment variable configuration helpers."""
from __future__ import annotations
import os
from dataclasses import dataclass


def required_env(name: str) -> str:
    """Read a required setting without exposing its value in an error."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable {name} is not set")
    return value


@dataclass(frozen=True)
class DatabaseSettings:
    driver: str
    host: str
    database: str
    username: str | None = None
    password: str | None = None
    port: int | None = None

    @classmethod
    def from_env(cls, prefix: str = "DB_") -> "DatabaseSettings":
        port = os.getenv(f"{prefix}PORT")
        return cls(
            driver=os.getenv(f"{prefix}DRIVER", "sqlite"),
            host=os.getenv(f"{prefix}HOST", ""),
            database=required_env(f"{prefix}NAME"),
            username=os.getenv(f"{prefix}USER"),
            password=os.getenv(f"{prefix}PASSWORD"),
            port=int(port) if port else None,
        )
