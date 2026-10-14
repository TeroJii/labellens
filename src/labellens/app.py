"""Top-level application controller."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from labellens.image_scanner import scan_images
from labellens.session import LabelingSession

_DISPLAY_MAX = (800, 500)


class App:
    """Main application class that owns the Tkinter root window."""

    def __init__(self) -> None:
        """Initialise the application and build the GUI."""
        self._root = tk.Tk()
        self._root.title("LabelLens")
        self._root.geometry("900x600")
        self._session: LabelingSession = LabelingSession()
        self._photo: ImageTk.PhotoImage | None = None
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

        nav = tk.Frame(self._root)
        nav.pack(side=tk.BOTTOM, pady=6)

        tk.Button(nav, text="← Previous", command=self._prev).pack(side=tk.LEFT, padx=4)
        tk.Button(nav, text="Next →", command=self._next).pack(side=tk.LEFT, padx=4)

        self._canvas = tk.Canvas(
            self._root, bg="#2b2b2b", cursor="crosshair"
        )
        self._canvas.pack(fill=tk.BOTH, expand=True)

    def _bind_keys(self) -> None:
        """Bind keyboard shortcuts."""
        self._root.bind("<Left>", lambda _e: self._prev())
        self._root.bind("<Right>", lambda _e: self._next())
        self._canvas.bind("<Configure>", lambda _e: self._display_current())

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
        self._session = LabelingSession(images=images)
        self._update_info()
        self._display_current()

    def _prev(self) -> None:
        """Navigate to the previous image."""
        if not self._session.images:
            return
        self._session.previous_image()
        self._update_info()
        self._display_current()

    def _next(self) -> None:
        """Navigate to the next image."""
        if not self._session.images:
            return
        self._session.next_image()
        self._update_info()
        self._display_current()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

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
            return
        try:
            img = Image.open(img_path)
        except Exception as exc:
            messagebox.showerror("Image error", str(exc))
            return

        cw = self._canvas.winfo_width() or _DISPLAY_MAX[0]
        ch = self._canvas.winfo_height() or _DISPLAY_MAX[1]
        img.thumbnail((cw, ch), Image.LANCZOS)

        self._photo = ImageTk.PhotoImage(img)
        self._canvas.create_image(cw // 2, ch // 2, anchor=tk.CENTER, image=self._photo)

    def run(self) -> None:
        """Start the Tkinter main-loop."""
        self._root.mainloop()
