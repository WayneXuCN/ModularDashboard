"""Main application entry point."""

import argparse

from .app import run_app


def main():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(description="Research Dashboard")
    parser.add_argument(
        "--native", action="store_true", help="Run as native desktop app"
    )
    args = parser.parse_args()

    run_app(native=args.native)


if __name__ == "__main__":
    main()
