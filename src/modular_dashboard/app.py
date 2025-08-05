"""Main application logic."""

import os
import pathlib
import platform
import sys
from typing import Any

from dotenv import load_dotenv
from loguru import logger
from nicegui import app, ui

from .config.manager import load_config
from .ui.dashboard import render_dashboard, render_module_detail


def initialize_app(config: dict[str, Any]) -> None:
    """Initialize the NiceGUI application.

    This function sets up the application-level configurations
    such as static files and CSS styles.

    Parameters
    ----------
    config : Dict[str, Any]
        The application configuration dictionary.
    """
    # logger.info(f"App config: {config}")

    # Add static files
    app.add_static_files("/static", "src/modular_dashboard/static")

    # Add custom CSS
    ui.add_head_html("""
        <link href="/static/css/style.css" rel="stylesheet">
    """)


def run_app(native: bool = False) -> None:
    """Run the Research Dashboard application.

    This function initializes and starts the Research Dashboard application
    with the specified configuration. It sets up the UI, loads configuration
    and starts the web server.

    Parameters
    ----------
    native : bool, default=False
        If True, runs the application as a native desktop application.
        If False, runs as a web application.

    Returns
    -------
    None

    Raises
    ------
    Exception
        If the application fails to start due to configuration or runtime errors.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Load configuration (cached)
        config = load_config()

        # Initialize the application
        initialize_app(config.__dict__)

        # Setup main dashboard page
        @ui.page("/")
        def main_page():
            render_dashboard(config)

        # Setup the dashboard UI routes
        @ui.page("/module/{module_id}")
        def module_detail_page(module_id: str):
            """Create a page for the module detail view."""
            render_module_detail(module_id, config)

        # Determine if we should enable auto-reload based on environment
        # Default to production environment if not specified
        environment = os.getenv("ENVIRONMENT", "production").lower()
        reload_enabled = environment == "development"

        # On Windows, set the WebView2 runtime path
        # Reference: https://learn.microsoft.com/zh-cn/microsoft-edge/webview2/concepts/distribution?tabs=dotnetcsharp#details-about-the-fixed-version-runtime-distribution-mode
        if native and platform.system() == "Windows":
            os.environ["WEBVIEW2_BROWSER_EXECUTABLE_FOLDER"] = str(
                pathlib.Path(__file__).parent.parent.parent
                / r"runtime\Microsoft.WebView2.FixedVersionRuntime.138.0.3351.121.x64"
            )

        # Run the application
        if native:
            ui.run(
                title="Dashboard",
                native=True,
                favicon="src/modular_dashboard/assets/img/favicon.ico",
                window_size=(1024, 786),
                reload=reload_enabled,  # Enable auto-reload based on environment
            )
        else:
            ui.run(
                title="Dashboard",
                favicon="src/modular_dashboard/assets/img/favicon.ico",
                reload=reload_enabled,  # Enable auto-reload based on environment
            )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise


run_app(native="--native" in sys.argv)
