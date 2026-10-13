"""Tests for image_scanner module."""

from pathlib import Path

import pytest

from labellens.image_scanner import scan_images


def test_scan_images_returns_sorted_list(tmp_path: Path) -> None:
    for name in ["b.jpg", "a.png", "c.jpeg"]:
        (tmp_path / name).touch()
    result = scan_images(tmp_path)
    assert [p.name for p in result] == ["a.png", "b.jpg", "c.jpeg"]


def test_scan_images_ignores_non_images(tmp_path: Path) -> None:
    (tmp_path / "image.jpg").touch()
    (tmp_path / "notes.txt").touch()
    result = scan_images(tmp_path)
    assert len(result) == 1


def test_scan_images_raises_on_missing_dir(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Not a directory"):
        scan_images(tmp_path / "nonexistent")


def test_scan_images_raises_on_empty_dir(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No supported images"):
        scan_images(tmp_path)
