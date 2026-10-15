"""Labeling session: tracks images, labels and annotations."""

from dataclasses import dataclass, field
from pathlib import Path


def parse_labels(raw: str) -> list[str]:
    """Parse and validate a comma-separated label string.

    Args:
        raw: Comma-separated label names entered by the user.

    Returns:
        A deduplicated, whitespace-trimmed list of labels.

    Raises:
        ValueError: If fewer than two distinct valid labels are provided.
    """
    seen: set[str] = set()
    labels: list[str] = []
    for part in raw.split(","):
        label = part.strip()
        if label and label not in seen:
            seen.add(label)
            labels.append(label)
    if len(labels) < 2:
        raise ValueError("At least two distinct labels are required.")
    return labels


@dataclass
class LabelingSession:
    """Holds the state of an active labeling session."""

    images: list[Path] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    annotations: dict[Path, str] = field(default_factory=dict)
    _current_index: int = field(default=0, init=False, repr=False)

    @property
    def current_image(self) -> Path | None:
        """Return the currently selected image path, or None if empty."""
        if not self.images:
            return None
        return self.images[self._current_index]

    def next_image(self) -> None:
        """Advance to the next image, wrapping around."""
        if self.images:
            self._current_index = (self._current_index + 1) % len(self.images)

    def previous_image(self) -> None:
        """Move to the previous image, wrapping around."""
        if self.images:
            self._current_index = (self._current_index - 1) % len(self.images)

    def assign_label(self, label: str) -> None:
        """Assign *label* to the current image."""
        if self.current_image is not None:
            self.annotations[self.current_image] = label

    def is_complete(self) -> bool:
        """Return True when every image has been labeled."""
        return bool(self.images) and all(
            img in self.annotations for img in self.images
        )
