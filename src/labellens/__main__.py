"""Entry point for the labellens CLI."""

from labellens.app import App


def main() -> None:
    """Launch the LabelLens application."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
