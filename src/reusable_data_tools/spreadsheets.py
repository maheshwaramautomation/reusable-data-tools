"""Excel conversion helpers. Requires the optional 'excel' dependencies."""
from __future__ import annotations
import csv
from pathlib import Path
from .files import clean_cell


def excel_to_tsv(source: str | Path, destination: str | Path, *, sheet: int | str = 0) -> int:
    """Convert a sheet to TSV while keeping rows in their original order."""
    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        raise RuntimeError("Install openpyxl to convert Excel files") from exc
    source, destination = Path(source), Path(destination)
    if source.suffix.lower() not in (".xlsx", ".xlsm"):
        raise ValueError("Supported Excel formats: .xlsx and .xlsm")
    wb = load_workbook(source, read_only=True, data_only=True)
    try:
        ws = wb.worksheets[sheet] if isinstance(sheet, int) else wb[sheet]
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream, delimiter="\t")
            count = 0
            for row in ws.iter_rows(values_only=True):
                writer.writerow([clean_cell(cell) for cell in row])
                count += 1
        return count
    finally:
        wb.close()
