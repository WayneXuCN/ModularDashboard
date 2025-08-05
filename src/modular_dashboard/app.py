"""Main application logic."""

import os
import pathlib
import platform
import sys
import time
from typing import Any

from dotenv import load_dotenv
from loguru import logger
from nicegui import app, ui

from .config.manager import load_config
from .ui.dashboard import render_dashboard, render_module_detail
from .ui.stats_dashboard import render_stats_dashboard
from .utils.system_monitor import get_performance_tracker

stats_collector = get_performance_tracker()


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

    # Initialize theme based on config
    if config.get("theme") == "dark":
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()


def run_app(native: bool = False) -> None:
    """Run the Modular Dashboard application.

    This function initializes and starts the Modular Dashboard application
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

        # Collect initial module statistics in development mode
        if os.getenv("ENVIRONMENT", "production").lower() == "development":
            import tracemalloc

            from .modules.registry import MODULE_REGISTRY

            tracemalloc.start()

            # Force initialization of all modules to collect stats
            for module_config in config.modules:
                module_class = MODULE_REGISTRY.get(module_config.id)
                if module_class:
                    try:
                        # Memory tracking
                        snapshot1 = tracemalloc.take_snapshot()

                        # High precision timing
                        start_time = time.perf_counter()
                        module_class(module_config.config)
                        init_time = time.perf_counter() - start_time

                        snapshot2 = tracemalloc.take_snapshot()
                        memory_usage = sum(
                            stat.size_diff
                            for stat in snapshot2.compare_to(snapshot1, "lineno")
                        )

                        stats_collector.record_init(
                            str(module_config.id), init_time, max(0, memory_usage)
                        )
                        logger.info(
                            f"Pre-initialized {module_config.id} in {init_time:.6f}s, memory: {memory_usage} bytes"
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to pre-initialize {module_config.id}: {e}"
                        )
                        # Still record failed attempts with 0 time
                        stats_collector.record_init(str(module_config.id), 0.0, 0)

            tracemalloc.stop()

        # Setup main dashboard page
        @ui.page("/")
        def main_page():
            render_dashboard(config)

        # Setup the dashboard UI routes
        @ui.page("/module/{module_id}")
        def module_detail_page(module_id: str):
            """Create a page for the module detail view."""
            render_module_detail(module_id, config)

        @ui.page("/stats")
        def stats_page():
            """Create a unified page for performance and memory statistics."""
            render_stats_dashboard()

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
