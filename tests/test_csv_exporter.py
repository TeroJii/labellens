"""Tests for csv_exporter module."""

import csv
from pathlib import Path

from labellens.csv_exporter import export_csv


def test_export_csv_writes_correct_content(tmp_path: Path) -> None:
    annotations = {
        Path("img_a.jpg"): "cat",
        Path("img_b.jpg"): "dog",
    }
    out = tmp_path / "labels.csv"
    export_csv(annotations, out)

    rows = list(csv.reader(out.read_text(encoding="utf-8").splitlines()))
    assert rows[0] == ["filename", "label"]
    assert ["img_a.jpg", "cat"] in rows
    assert ["img_b.jpg", "dog"] in rows


def test_export_csv_empty_annotations(tmp_path: Path) -> None:
    out = tmp_path / "labels.csv"
    export_csv({}, out)
    rows = list(csv.reader(out.read_text(encoding="utf-8").splitlines()))
    assert rows == [["filename", "label"]]
