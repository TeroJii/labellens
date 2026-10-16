"""Tests for the LabelingSession class."""

from pathlib import Path

from labellens.session import LabelingSession


def _make_session(n: int = 3) -> LabelingSession:
    images = [Path(f"img_{i}.jpg") for i in range(n)]
    return LabelingSession(images=images, labels=["cat", "dog"])


def test_current_image_initially_first() -> None:
    session = _make_session()
    assert session.current_image == Path("img_0.jpg")


def test_next_image_advances() -> None:
    session = _make_session()
    session.next_image()
    assert session.current_image == Path("img_1.jpg")


def test_next_image_wraps() -> None:
    session = _make_session(2)
    session.next_image()
    session.next_image()
    assert session.current_image == Path("img_0.jpg")


def test_previous_image_wraps() -> None:
    session = _make_session(3)
    session.previous_image()
    assert session.current_image == Path("img_2.jpg")


def test_assign_label() -> None:
    session = _make_session()
    session.assign_label("cat")
    assert session.annotations[Path("img_0.jpg")] == "cat"


def test_set_labels_preserves_navigation_state() -> None:
    session = _make_session(3)
    session.next_image()
    session.next_image()
    session.assign_label("dog")
    session.set_labels(["cat", "dog", "other"])
    assert session.current_image == Path("img_2.jpg")
    assert session.annotations[Path("img_2.jpg")] == "dog"
    assert session.labels == ["cat", "dog", "other"]


def test_is_complete_false_when_unlabeled() -> None:
    session = _make_session()
    assert not session.is_complete()


def test_is_complete_true_when_all_labeled() -> None:
    session = _make_session(2)
    for img in session.images:
        session.annotations[img] = "cat"
    assert session.is_complete()


def test_progress_initially_zero() -> None:
    session = _make_session(3)
    labeled, total = session.progress()
    assert labeled == 0
    assert total == 3


def test_progress_increments_with_labels() -> None:
    session = _make_session(3)
    session.assign_label("cat")
    labeled, total = session.progress()
    assert labeled == 1
    assert total == 3


def test_progress_complete() -> None:
    session = _make_session(2)
    session.assign_label("cat")
    session.next_image()
    session.assign_label("cat")
    labeled, total = session.progress()
    assert labeled == total == 2


