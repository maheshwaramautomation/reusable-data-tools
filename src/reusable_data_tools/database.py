"""Minimal reusable DB-API connection factory. Install drivers only when needed."""
from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from collections.abc import Iterator
from typing import Any
from .config import DatabaseSettings


def connect(settings: DatabaseSettings) -> Any:
    """Connect to SQLite, Microsoft SQL Server, or MySQL; callers own the connection."""
    driver = settings.driver.casefold()
    if driver in ("sqlite", "sqlite3"):
        return sqlite3.connect(settings.database)
    if driver in ("sqlserver", "mssql", "sql_server"):
        try:
            import pyodbc
        except ImportError as exc:
            raise RuntimeError("Install pyodbc to use SQL Server") from exc
        fields = ["DRIVER={ODBC Driver 18 for SQL Server}", f"SERVER={settings.host}", f"DATABASE={settings.database}", "Encrypt=yes"]
        if settings.port:
            fields[1] += f",{settings.port}"
        if settings.username:
            fields += [f"UID={settings.username}", f"PWD={settings.password or ''}"]
        else:
            fields.append("Trusted_Connection=yes")
        return pyodbc.connect(";".join(fields) + ";")
    if driver in ("mysql", "mariadb"):
        try:
            import pymysql
        except ImportError as exc:
            raise RuntimeError("Install pymysql to use MySQL") from exc
        return pymysql.connect(host=settings.host, user=settings.username, password=settings.password,
                               database=settings.database, port=settings.port or 3306)
    raise ValueError(f"Unsupported database driver: {settings.driver}")


@contextmanager
def transaction(settings: DatabaseSettings) -> Iterator[Any]:
    """Commit successful operations, roll back on failure, and always close."""
    connection = connect(settings)
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
