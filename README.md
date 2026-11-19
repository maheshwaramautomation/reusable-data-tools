# Reusable Data Tools

A portable Python library for data processing, database connections, Excel transformation, SMTP notifications, and Vault integration.

## Install

Requires Python 3.10 or later.

```bash
python -m pip install -e .
python -m pip install -e '.[excel]'
python -m unittest discover -s tests -v
```

## Package layout

- `src/reusable_data_tools/config.py`: environment configuration and database settings
- `src/reusable_data_tools/database.py`: SQLite, SQL Server, and MySQL connectors, transactions
- `src/reusable_data_tools/files.py`: CSV/TSV conversion, data cleanup, header reading
- `src/reusable_data_tools/spreadsheets.py`: Excel sheet to TSV
- `src/reusable_data_tools/mail.py`: SMTP with verified TLS
- `src/reusable_data_tools/vault.py`: Vault AppRole login and KV v2 retrieval
- `tests/test_core.py`: core tests

## Quick example

```python
from reusable_data_tools import convert_delimited, read_header, excel_to_tsv

count = convert_delimited("customers.csv", "output/customers.tsv")
print(count, read_header("output/customers.tsv"))
excel_to_tsv("report.xlsx", "output/report.tsv")
```

## Configuration

Set environment variables through your deployment platform or local environment. See `.env.example` for names. The package reads environment variables directly; it does not automatically parse `.env` files. Never commit passwords, tokens, or local `.env` files.

```python
from reusable_data_tools import DatabaseSettings, transaction

settings = DatabaseSettings.from_env()
with transaction(settings) as connection:
    print(connection.execute("SELECT 1").fetchone())
```

## Scope

This public repository contains the extracted reusable core only. Older workflow-specific modules from the original codebase are intentionally not published pending independent dependency, licensing, and security review.
