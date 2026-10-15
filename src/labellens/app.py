"""Top-level application controller."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from labellens.image_scanner import scan_images
from labellens.session import LabelingSession, parse_labels

_DISPLAY_MAX = (800, 500)


class App:
    """Main application class that owns the Tkinter root window."""

    def __init__(self) -> None:
        """Initialise the application and build the GUI."""
        self._root = tk.Tk()
        self._root.title("LabelLens")
        self._root.geometry("900x700")
        self._session: LabelingSession = LabelingSession()
        self._photo: ImageTk.PhotoImage | None = None
        self._loaded_image: Image.Image | None = None
        self._loaded_image_path: Path | None = None
        self._label_var = tk.StringVar()
        self._build_ui()
        self._bind_keys()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        """Build all widgets."""
        toolbar = tk.Frame(self._root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=8, pady=4)

        tk.Button(toolbar, text="Open Folder…", command=self._open_folder).pack(
            side=tk.LEFT
        )

        self._info_var = tk.StringVar(value="No folder selected")
        tk.Label(toolbar, textvariable=self._info_var).pack(side=tk.LEFT, padx=12)

        # Label definition row
        label_row = tk.Frame(self._root)
        label_row.pack(side=tk.TOP, fill=tk.X, padx=8, pady=2)

        tk.Label(label_row, text="Labels (comma-separated):").pack(side=tk.LEFT)
        self._labels_entry = tk.Entry(label_row, width=40)
        self._labels_entry.pack(side=tk.LEFT, padx=4)
        tk.Button(label_row, text="Set Labels", command=self._set_labels).pack(
            side=tk.LEFT
        )

        # Dynamic label buttons area
        self._label_buttons_frame = tk.Frame(self._root)
        self._label_buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=8, pady=2)

        nav = tk.Frame(self._root)
        nav.pack(side=tk.BOTTOM, pady=6)

        tk.Button(nav, text="← Previous", command=self._prev).pack(side=tk.LEFT, padx=4)
        tk.Button(nav, text="Next →", command=self._next).pack(side=tk.LEFT, padx=4)

        self._canvas = tk.Canvas(
            self._root, bg="#2b2b2b", cursor="crosshair"
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

    def _rebuild_label_buttons(self) -> None:
        """Destroy and recreate label buttons from current session labels."""
        for widget in self._label_buttons_frame.winfo_children():
            widget.destroy()

        self._label_var.set("")
        labels = self._session.labels
        if not labels:
            return

        tk.Label(self._label_buttons_frame, text="Assign:").pack(side=tk.LEFT)

        for i, label in enumerate(labels):
            shortcut = str(i + 1) if i < 9 else ""
            text = f"[{shortcut}] {label}" if shortcut else label
            tk.Radiobutton(
                self._label_buttons_frame,
                text=text,
                variable=self._label_var,
                value=label,
                command=lambda lbl=label: self._assign_label(lbl),
            ).pack(side=tk.LEFT, padx=4)

    def _bind_keys(self) -> None:
        """Bind keyboard shortcuts."""
        self._root.bind("<Left>", lambda _e: self._prev())
        self._root.bind("<Right>", lambda _e: self._next())
        self._canvas.bind("<Configure>", lambda _e: self._display_current())
        for i in range(1, 10):
            self._root.bind(
                str(i),
                lambda _e, idx=i - 1: self._select_label_by_index(idx),
            )
        self._root.bind("<Control-s>", lambda _e: self._export())

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _open_folder(self) -> None:
        """Ask the user for a folder and load images from it."""
        folder = filedialog.askdirectory(title="Select image folder")
        if not folder:
            return
        try:
            images = scan_images(Path(folder))
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
            return
        self._session = LabelingSession(images=images, labels=self._session.labels)
        self._update_info()
        self._display_current()
        self._restore_label_selection()

    def _set_labels(self) -> None:
        """Validate and apply the labels entered by the user."""
        raw = self._labels_entry.get()
        try:
            labels = parse_labels(raw)
        except ValueError as exc:
            messagebox.showerror("Invalid labels", str(exc))
            return
        self._session = LabelingSession(
            images=self._session.images,
            labels=labels,
            annotations=self._session.annotations,
        )
        self._rebuild_label_buttons()
        self._restore_label_selection()

    def _assign_label(self, label: str) -> None:
        """Assign *label* to the current image."""
        self._session.assign_label(label)

    def _select_label_by_index(self, idx: int) -> None:
        """Select the label at *idx* (0-based) using a keyboard shortcut."""
        if idx < len(self._session.labels):
            label = self._session.labels[idx]
            self._label_var.set(label)
            self._assign_label(label)

    def _prev(self) -> None:
        """Navigate to the previous image."""
        if not self._session.images:
            return
        self._session.previous_image()
        self._update_info()
        self._display_current()
        self._restore_label_selection()

    def _next(self) -> None:
        """Navigate to the next image."""
        if not self._session.images:
            return
        self._session.next_image()
        self._update_info()
        self._display_current()
        self._restore_label_selection()

    def _export(self) -> None:
        """Export annotations to CSV."""
        from labellens.csv_exporter import export_csv

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save annotations",
        )
        if not path:
            return
        try:
            export_csv(self._session.annotations, Path(path))
            messagebox.showinfo("Exported", f"Annotations saved to {path}")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _restore_label_selection(self) -> None:
        """Set the radio-button selection to the previously assigned label."""
        current = self._session.current_image
        if current is not None and current in self._session.annotations:
            self._label_var.set(self._session.annotations[current])
        else:
            self._label_var.set("")

    def _update_info(self) -> None:
        """Refresh the filename / count label in the toolbar."""
        images = self._session.images
        if not images:
            self._info_var.set("No folder selected")
            return
        idx = images.index(self._session.current_image)  # type: ignore[arg-type]
        name = self._session.current_image.name  # type: ignore[union-attr]
        self._info_var.set(f"{name}  [{idx + 1} / {len(images)}]")

    def _display_current(self) -> None:
        """Render the current image on the canvas."""
        self._canvas.delete("all")
        img_path = self._session.current_image
        if img_path is None:
            self._loaded_image = None
            self._loaded_image_path = None
            return

        if img_path != self._loaded_image_path:
            try:
                self._loaded_image = Image.open(img_path)
            except Exception as exc:
                messagebox.showerror("Image error", str(exc))
                self._loaded_image = None
                self._loaded_image_path = None
                return
            self._loaded_image_path = img_path

        if self._loaded_image is None:
            return

        cw = self._canvas.winfo_width()
        ch = self._canvas.winfo_height()
        if cw <= 1:
            cw = _DISPLAY_MAX[0]
        if ch <= 1:
            ch = _DISPLAY_MAX[1]

        img = self._loaded_image.copy()
        img.thumbnail((cw, ch), Image.LANCZOS)

        self._photo = ImageTk.PhotoImage(img)
        self._canvas.create_image(cw // 2, ch // 2, anchor=tk.CENTER, image=self._photo)

    def run(self) -> None:
        """Start the Tkinter main-loop."""
        self._root.mainloop()
