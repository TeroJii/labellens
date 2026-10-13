"""Scan a directory for supported image files."""

from pathlib import Path

SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(
    {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
)


def scan_images(folder: Path) -> list[Path]:
    """Return a sorted list of image paths found directly inside *folder*.

    Args:
        folder: Directory to search.

    Returns:
        Sorted list of image :class:`~pathlib.Path` objects.

    Raises:
        ValueError: If *folder* is not a directory or contains no images.
    """
    if not folder.is_dir():
        raise ValueError(f"Not a directory: {folder}")

    images = sorted(
        p for p in folder.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not images:
        raise ValueError(f"No supported images found in: {folder}")

    return images
