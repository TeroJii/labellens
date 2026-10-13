"""Export annotations to a CSV file."""

import csv
from pathlib import Path


def export_csv(annotations: dict[Path, str], output_path: Path) -> None:
    """Write *annotations* to a CSV file at *output_path*.

    The CSV contains two columns: ``filename`` and ``label``.

    Args:
        annotations: Mapping of image path to label string.
        output_path: Destination CSV file path.

    Raises:
        OSError: If the file cannot be written.
    """
    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["filename", "label"])
        for image_path, label in annotations.items():
            writer.writerow([image_path.name, label])
