# Copilot Instructions

## Project Overview

This project is a desktop application for labeling image datasets for machine learning classification tasks.

The application shall:

- Display images from a user-selected folder.
- Allow the user to define a set of permitted class labels.
- Allow exactly one label per image.
- Store labels in memory during the session.
- Export annotations to a CSV file with columns:

```csv
filename,label
image1.jpg,class_a
image2.jpg,class_b
```

The application is intended for small to medium-sized image classification datasets and should remain lightweight and easy to install.

---

## Technical Stack

Use:

- Python 3.12+
- Tkinter for GUI
- Pillow (PIL) for image handling
- pathlib for filesystem operations
- csv module for CSV export
- pytest for testing
- Ruff for linting
- Black for formatting

Do not introduce heavy dependencies unless there is a clear benefit.

Preferred dependency footprint:

```text
Pillow
```

---

## Architecture Principles

Keep GUI code separate from business logic.

Recommended layer structure:

```text
gui/
    presentation and user interaction

core/
    labeling session logic
    validation
    domain models

io/
    file scanning
    image loading
    csv export
```

The GUI should never directly manipulate annotation data structures.

Business logic should be testable without opening the GUI.

---

## Coding Style

- Use type hints everywhere.
- Prefer pathlib.Path over os.path.
- Prefer dataclasses for simple data containers.
- Keep functions small and focused.
- Avoid global state.
- Use descriptive variable names.
- Follow PEP8.
- Write docstrings for public classes and functions.

Example:

```python
def assign_label(image_path: Path, label: str) -> None:
    """Assign a class label to an image."""
```

---

## GUI Guidelines

The GUI should remain simple and keyboard-friendly.

Required functionality:

- Select image folder
- Enter permitted labels
- Display current image
- Assign label
- Previous image
- Next image
- Export CSV

Preferred shortcuts:

```text
Left Arrow     Previous image
Right Arrow    Next image
1..9           Select label
Ctrl+S         Save/export
```

The application should preserve image aspect ratio when displaying images.

Never modify original image files.

---

## Label Management

Labels should be defined by the user.

Example:

```text
cat,dog,other
```

After validation:

```python
[
    "cat",
    "dog",
    "other",
]
```

Requirements:

- Remove duplicates
- Trim whitespace
- Reject empty labels
- Require at least two labels

---

## CSV Export

Export only:

```csv
filename,label
```

Example output:

```csv
filename, label
IMG_001.jpg,cat
IMG_002.jpg,dog
```

Use filenames rather than absolute paths whenever possible.

---

## Error Handling

Prefer user-friendly messages over stack traces.

Handle:

- Empty folders
- Unsupported image formats
- Missing files
- CSV write failures
- Invalid label definitions

---

## Testing Expectations

Create unit tests for:

- label parsing
- session navigation
- label assignment
- completeness checks
- CSV export

GUI tests are optional.

Prioritize testing business logic over UI code.

---

## Future Extensions

Design code so that the following can be added later without major refactoring:

- Multi-class labeling
- Object detection annotations
- Segmentation masks
- Autosave
- Resume previous session
- Keyboard-only workflows
- Image prefetching
- Train/validation/test split export

Favor extensibility, but keep the initial implementation simple.