#!/usr/bin/env python3
"""Tests for inspect_workbook.py using a synthetic workbook in a temp directory."""

from __future__ import annotations

import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

from inspect_workbook import inspect_workbook, main


WORKBOOK_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Requirements" sheetId="1" r:id="rId1"/>
    <sheet name="Lookup" sheetId="2" state="hidden" r:id="rId2"/>
  </sheets>
</workbook>
"""

RELATIONSHIPS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Target="worksheets/sheet1.xml"
   Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"/>
  <Relationship Id="rId2" Target="worksheets/sheet2.xml"
   Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"/>
</Relationships>
"""

SHARED_STRINGS_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 count="2" uniqueCount="2">
  <si><t>Requirement</t></si>
  <si><t>User can export</t></si>
</sst>
"""

SHEET1_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="A1:B3"/>
  <cols><col min="4" max="4" hidden="1"/></cols>
  <sheetData>
    <row r="1"><c r="A1" t="s" s="1"><v>0</v></c></row>
    <row r="2"><c r="B2" t="s" s="2"><v>1</v></c></row>
    <row r="3" hidden="1"><c r="A3"><f>1+1</f><v>2</v></c></row>
  </sheetData>
  <mergeCells count="1"><mergeCell ref="A1:B1"/></mergeCells>
</worksheet>
"""

SHEET2_XML = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="A1"/>
  <sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>X</t></is></c></row></sheetData>
</worksheet>
"""


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def create_workbook(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("xl/workbook.xml", WORKBOOK_XML)
        archive.writestr("xl/_rels/workbook.xml.rels", RELATIONSHIPS_XML)
        archive.writestr("xl/sharedStrings.xml", SHARED_STRINGS_XML)
        archive.writestr("xl/worksheets/sheet1.xml", SHEET1_XML)
        archive.writestr("xl/worksheets/sheet2.xml", SHEET2_XML)


class InspectWorkbookTests(unittest.TestCase):
    def test_inspection_preserves_file_and_emits_traceable_locations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "requirements.xlsx"
            create_workbook(workbook)
            before = file_hash(workbook)

            result = inspect_workbook(workbook, source_key="BIZ")

            self.assertEqual(before, file_hash(workbook))
            self.assertEqual(result["sha256"], before)
            self.assertEqual(len(result["sheets"]), 2)
            requirements = result["sheets"][0]
            self.assertEqual(requirements["merged_ranges"], ["A1:B1"])
            self.assertEqual(requirements["hidden_rows"], [3])
            self.assertEqual(requirements["hidden_columns"], [{"min": 4, "max": 4}])
            export_cell = next(
                cell for cell in requirements["cells"] if cell["cell"] == "B2"
            )
            self.assertEqual(export_cell["value"], "User can export")
            self.assertEqual(export_cell["src_id"], "SRC-BIZ-REQUIREMENTS-R2-C2")
            self.assertEqual(result["sheets"][1]["state"], "hidden")

    def test_rejects_legacy_xls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "requirements.xls"
            workbook.write_bytes(b"legacy")
            with self.assertRaisesRegex(ValueError, "Only .xlsx and .xlsm"):
                inspect_workbook(workbook)

    def test_cli_filters_sheet_and_emits_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "requirements.xlsx"
            create_workbook(workbook)
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        str(workbook),
                        "--source-key",
                        "BIZ",
                        "--sheet",
                        "Requirements",
                        "--max-cells",
                        "1",
                    ]
                )

            self.assertEqual(exit_code, 0)
            result = json.loads(stdout.getvalue())
            self.assertEqual(
                [sheet["name"] for sheet in result["sheets"]], ["Requirements"]
            )
            self.assertTrue(result["sheets"][0]["truncated"])
            self.assertEqual(result["sheets"][0]["returned_cells"], 1)

    def test_rejects_unknown_sheet(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "requirements.xlsx"
            create_workbook(workbook)
            with self.assertRaisesRegex(ValueError, "Unknown sheet"):
                inspect_workbook(workbook, selected_sheets={"Missing"})


if __name__ == "__main__":
    unittest.main()
