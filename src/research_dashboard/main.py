"""Main application logic."""

import argparse

from nicegui import ui

from .config.manager import load_config
from .ui.dashboard import render_dashboard
from .utils.logger import get_logger

logger = get_logger(__name__)


def run_app(native=False):
    """Run the Research Dashboard application."""
    try:
        # Load configuration
        config = load_config()

        # Add custom CSS
        ui.add_head_html("""
            <link href="static/css/style.css" rel="stylesheet">
        """)

        # Setup the dashboard UI
        render_dashboard(config)

        # Run the application
        if native:
            ui.run(
                title="Research Dashboard",
                native=True,
                window_size=(1200, 800),
                reload=False,
            )
        else:
            ui.run(title="Research Dashboard", reload=False)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Research Dashboard")
    parser.add_argument(
        "--native", action="store_true", help="Run as native desktop app"
    )
    args = parser.parse_args()

    run_app(native=args.native)
