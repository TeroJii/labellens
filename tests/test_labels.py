"""Tests for the parse_labels function."""

import pytest

from labellens.session import parse_labels


def test_parse_labels_basic() -> None:
    assert parse_labels("cat,dog") == ["cat", "dog"]


def test_parse_labels_trims_whitespace() -> None:
    assert parse_labels("  cat , dog , other ") == ["cat", "dog", "other"]


def test_parse_labels_removes_duplicates() -> None:
    assert parse_labels("cat,dog,cat") == ["cat", "dog"]


def test_parse_labels_skips_empty_parts() -> None:
    assert parse_labels("cat,,dog") == ["cat", "dog"]


def test_parse_labels_raises_when_fewer_than_two() -> None:
    with pytest.raises(ValueError, match="At least two"):
        parse_labels("cat")


def test_parse_labels_raises_on_empty_string() -> None:
    with pytest.raises(ValueError, match="At least two"):
        parse_labels("")


def test_parse_labels_raises_when_duplicates_leave_one() -> None:
    with pytest.raises(ValueError, match="At least two"):
        parse_labels("cat,cat,cat")
