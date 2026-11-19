"""Portable delimited-file conversion and cleanup."""
from __future__ import annotations
import csv
import re
from pathlib import Path


def clean_cell(value: object) -> str:
    """Normalize newlines and remove NUL characters from a cell."""
    if value is None:
        return ""
    return re.sub(r"[\r\n]+", " ", str(value).replace("\x00", "")).strip()


def convert_delimited(source: str | Path, destination: str | Path, *,
                      source_delimiter: str = ",", output_delimiter: str = "\t",
                      encoding: str = "utf-8-sig") -> int:
    """Stream a CSV/TSV file to another delimiter; return written row count."""
    source, destination = Path(source), Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with source.open("r", newline="", encoding=encoding) as inp, destination.open(
        "w", newline="", encoding="utf-8"
    ) as out:
        reader = csv.reader(inp, delimiter=source_delimiter)
        writer = csv.writer(out, delimiter=output_delimiter)
        for row in reader:
            writer.writerow([clean_cell(c) for c in row])
            count += 1
    return count


def read_header(path: str | Path, delimiter: str | None = None) -> list[str]:
    """Return column names for CSV, TSV or Excel files."""
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            from openpyxl import load_workbook
        except ImportError as exc:
            raise RuntimeError("Install openpyxl to read Excel headers") from exc
        workbook = load_workbook(path, read_only=True, data_only=True)
        try:
            row = next(workbook.active.iter_rows(max_row=1, values_only=True), ())
            return [clean_cell(value) for value in row]
        finally:
            workbook.close()
    if delimiter is None:
        delimiter = "\t" if path.suffix.lower() in (".tab", ".tsv") else ","
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return next(csv.reader(f, delimiter=delimiter), [])
