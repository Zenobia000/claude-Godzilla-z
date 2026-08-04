#!/usr/bin/env python3
"""Read-only structural inspection of OOXML Excel workbooks."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any
from xml.etree import ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": DOC_REL_NS, "p": PKG_REL_NS}
CELL_REF = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")


def configure_utf8_stdio() -> None:
    """Keep JSON and errors valid on Windows consoles that default to cp950."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(value: str, fallback: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", value.upper())
    return "-".join(tokens) or fallback


def column_number(letters: str) -> int:
    number = 0
    for char in letters:
        number = number * 26 + ord(char) - ord("A") + 1
    return number


def all_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(node.text or "" for node in element.iter(f"{{{MAIN_NS}}}t"))


def load_shared_strings(workbook: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return [all_text(item) for item in root.findall("m:si", NS)]


def relationship_targets(workbook: zipfile.ZipFile) -> dict[str, str]:
    root = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
    targets: dict[str, str] = {}
    for relation in root.findall("p:Relationship", NS):
        relation_id = relation.attrib.get("Id")
        target = relation.attrib.get("Target")
        if (
            not relation_id
            or not target
            or relation.attrib.get("TargetMode") == "External"
        ):
            continue
        if target.startswith("/"):
            normalized = target.lstrip("/")
        else:
            normalized = str(PurePosixPath("xl") / PurePosixPath(target))
        targets[relation_id] = posixpath.normpath(normalized)
    return targets


def cell_value(cell: ET.Element, shared_strings: list[str]) -> tuple[Any, str]:
    cell_type = cell.attrib.get("t", "n")
    value_node = cell.find("m:v", NS)
    raw_value = value_node.text if value_node is not None else None

    if cell_type == "inlineStr":
        return all_text(cell.find("m:is", NS)), "inline-string"
    if cell_type == "s" and raw_value is not None:
        try:
            return shared_strings[int(raw_value)], "shared-string"
        except (ValueError, IndexError):
            return raw_value, "invalid-shared-string-index"
    if cell_type == "b":
        return raw_value == "1", "boolean"
    if cell_type == "e":
        return raw_value, "error"
    if cell_type == "str":
        return raw_value, "formula-string"
    return raw_value, "raw-number-or-date"


def inspect_sheet(
    workbook: zipfile.ZipFile,
    sheet_path: str,
    sheet_name: str,
    sheet_index: int,
    sheet_state: str,
    source_key: str,
    shared_strings: list[str],
    max_cells: int,
) -> dict[str, Any]:
    root = ET.fromstring(workbook.read(sheet_path))
    dimension = root.find("m:dimension", NS)
    merged = [
        node.attrib["ref"]
        for node in root.findall("m:mergeCells/m:mergeCell", NS)
        if "ref" in node.attrib
    ]
    hidden_rows = [
        int(row.attrib["r"])
        for row in root.findall("m:sheetData/m:row", NS)
        if row.attrib.get("hidden") in {"1", "true"} and "r" in row.attrib
    ]
    hidden_columns = [
        {
            "min": int(column.attrib.get("min", "0")),
            "max": int(column.attrib.get("max", "0")),
        }
        for column in root.findall("m:cols/m:col", NS)
        if column.attrib.get("hidden") in {"1", "true"}
    ]

    sheet_key = slug(sheet_name, f"S{sheet_index}")
    cells: list[dict[str, Any]] = []
    total_nonempty = 0

    for cell in root.findall("m:sheetData/m:row/m:c", NS):
        reference = cell.attrib.get("r", "")
        match = CELL_REF.match(reference)
        if not match:
            continue
        formula_node = cell.find("m:f", NS)
        formula = formula_node.text if formula_node is not None else None
        value, value_kind = cell_value(cell, shared_strings)
        if value in {None, ""} and formula is None:
            continue
        total_nonempty += 1
        if max_cells > 0 and len(cells) >= max_cells:
            continue
        letters, row_text = match.groups()
        row_number = int(row_text)
        column = column_number(letters)
        cells.append(
            {
                "source_file": None,
                "sheet": sheet_name,
                "row": row_number,
                "cell": reference,
                "src_id": f"SRC-{source_key}-{sheet_key}-R{row_number}-C{column}",
                "value": value,
                "value_kind": value_kind,
                "formula": formula,
                "style_id": cell.attrib.get("s"),
            }
        )

    return {
        "name": sheet_name,
        "index": sheet_index,
        "state": sheet_state,
        "path": sheet_path,
        "dimension": dimension.attrib.get("ref") if dimension is not None else None,
        "merged_ranges": merged,
        "hidden_rows": hidden_rows,
        "hidden_columns": hidden_columns,
        "total_nonempty_cells": total_nonempty,
        "returned_cells": len(cells),
        "truncated": max_cells > 0 and total_nonempty > len(cells),
        "cells": cells,
    }


def inspect_workbook(
    source: Path,
    source_key: str | None = None,
    selected_sheets: set[str] | None = None,
    max_cells: int = 5000,
) -> dict[str, Any]:
    source = source.resolve()
    if source.suffix.lower() not in {".xlsx", ".xlsm"}:
        raise ValueError(
            "Only .xlsx and .xlsm are supported; do not convert or rewrite legacy .xls."
        )
    if not source.is_file():
        raise FileNotFoundError(source)

    digest = sha256_file(source)
    selected_source_key = slug(source_key or source.stem, "WORKBOOK")
    used_default_key = source_key is None

    with zipfile.ZipFile(source, "r") as workbook:
        shared_strings = load_shared_strings(workbook)
        targets = relationship_targets(workbook)
        workbook_root = ET.fromstring(workbook.read("xl/workbook.xml"))
        sheet_records = []
        found_sheets: set[str] = set()
        for index, sheet in enumerate(
            workbook_root.findall("m:sheets/m:sheet", NS), start=1
        ):
            name = sheet.attrib.get("name", f"Sheet{index}")
            if selected_sheets and name not in selected_sheets:
                continue
            found_sheets.add(name)
            relation_id = sheet.attrib.get(f"{{{DOC_REL_NS}}}id")
            if not relation_id or relation_id not in targets:
                continue
            record = inspect_sheet(
                workbook=workbook,
                sheet_path=targets[relation_id],
                sheet_name=name,
                sheet_index=index,
                sheet_state=sheet.attrib.get("state", "visible"),
                source_key=selected_source_key,
                shared_strings=shared_strings,
                max_cells=max_cells,
            )
            for cell in record["cells"]:
                cell["source_file"] = str(source)
            sheet_records.append(record)
        missing_sheets = (selected_sheets or set()) - found_sheets
        if missing_sheets:
            missing = ", ".join(sorted(missing_sheets))
            raise ValueError(f"Unknown sheet name(s): {missing}")

    return {
        "source_file": str(source),
        "sha256": digest,
        "size_bytes": source.stat().st_size,
        "source_key": selected_source_key,
        "source_key_is_default": used_default_key,
        "source_key_warning": (
            "Default key is filename-derived; provide --source-key for a stable project identity."
            if used_default_key
            else None
        ),
        "inspection_mode": "read-only OOXML structure; not a visual render",
        "sheets": sheet_records,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect .xlsx/.xlsm structure without modifying the workbook."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument(
        "--source-key", help="Immutable project key used in SRC-ID values."
    )
    parser.add_argument(
        "--sheet",
        action="append",
        default=[],
        help="Inspect only this sheet; repeat to select multiple sheets.",
    )
    parser.add_argument(
        "--max-cells",
        type=int,
        default=5000,
        help="Maximum non-empty cells returned per sheet; 0 returns all.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_utf8_stdio()
    args = build_parser().parse_args(argv)
    if args.max_cells < 0:
        print("error: --max-cells must be zero or greater", file=sys.stderr)
        return 2
    try:
        result = inspect_workbook(
            source=args.workbook,
            source_key=args.source_key,
            selected_sheets=set(args.sheet) or None,
            max_cells=args.max_cells,
        )
    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        zipfile.BadZipFile,
        ET.ParseError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
