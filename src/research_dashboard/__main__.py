"""Main application entry point."""

from .app import run_app


def main():
    """Entry point for the application."""
    run_app(native=True)


if __name__ == "__main__":
    main()