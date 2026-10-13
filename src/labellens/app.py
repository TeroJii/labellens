"""Top-level application controller."""

import tkinter as tk


class App:
    """Main application class that owns the Tkinter root window."""

    def __init__(self) -> None:
        """Initialise the application and build the GUI."""
        self._root = tk.Tk()
        self._root.title("LabelLens")
        self._root.geometry("900x600")

    def run(self) -> None:
        """Start the Tkinter main-loop."""
        self._root.mainloop()
