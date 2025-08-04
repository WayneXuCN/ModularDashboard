"""Extended module base class with extended functionality."""

from collections.abc import Callable
from datetime import datetime
from typing import Any

from loguru import logger
from nicegui import ui

from .base import Module


class ExtendedModule(Module):
    """Extended module with additional functionality.

    This class extends the basic Module class with additional features
    commonly needed by more complex modules. It provides statistics
    tracking, retry logic, configuration management, data import/export,
    and UI components for module management.

    Parameters
    ----------
    config : dict[str, Any] | None, default=None
        Optional dictionary containing module-specific configuration.

    Attributes
    ----------
    config : dict[str, Any]
        Configuration dictionary for the module.
    """

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self._refresh_callbacks: list[Callable] = []
        self._error_handlers: list[Callable] = []
        self._is_initialized = False
        self._last_error: Exception | None = None
        self._stats: dict[str, Any] = {
            "fetch_count": 0,
            "error_count": 0,
            "last_fetch": None,
            "last_error": None,
        }

    @property
    def version(self) -> str:
        """Module version.

        Returns the current version of the module. Defaults to "1.0.0"
        but can be overridden by subclasses.

        Returns
        -------
        str
            Semantic version string (e.g., "1.0.0").
        """
        return "1.0.0"

    @property
    def category(self) -> str:
        """Module category.

        Returns the category this module belongs to. Used for
        organizing modules in the UI.

        Returns
        -------
        str
            Category name (default: "general").
        """
        return "general"

    @property
    def supported_features(self) -> list[str]:
        """List of supported features.

        Returns a list of feature identifiers that this module supports.
        Can be used by the UI to enable/disable certain functionality.

        Returns
        -------
        list[str]
            List of supported feature identifiers.
        """
        return []

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration for the module.

        Returns the default configuration values for this module.
        Subclasses should override this to provide module-specific
        default values.

        Returns
        -------
        dict[str, Any]
            Dictionary containing default configuration values.
        """
        return {}

    def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate module configuration.

        Validate that the provided configuration is valid for this module.
        Subclasses should override this to implement module-specific
        validation logic.

        Parameters
        ----------
        config : dict[str, Any]
            Configuration dictionary to validate.

        Returns
        -------
        bool
            True if configuration is valid, False otherwise.
        """
        return True

    def get_config_schema(self) -> dict[str, Any]:
        """Get configuration schema for UI generation.

        Returns a schema describing the configuration options for this
        module. This schema is used to automatically generate configuration
        UI elements.

        Returns
        -------
        dict[str, Any]
            Configuration schema with field definitions.
        """
        return {}

    def add_refresh_callback(self, callback: Callable) -> None:
        """Add a callback to be called when data is refreshed.

        Register a callback function that will be called whenever
        the module's data is refreshed.

        Parameters
        ----------
        callback : Callable
            Function to call when data is refreshed.
        """
        self._refresh_callbacks.append(callback)

    def add_error_handler(self, handler: Callable) -> None:
        """Add an error handler.

        Register an error handler function that will be called
        whenever an error occurs in the module.

        Parameters
        ----------
        handler : Callable
            Function to call when an error occurs.
        """
        self._error_handlers.append(handler)

    def _notify_refresh(self) -> None:
        """Notify all refresh callbacks.

        Call all registered refresh callbacks. Errors in callbacks
        are caught and logged but don't stop the notification process.
        """
        for callback in self._refresh_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in refresh callback: {e}")

    def _handle_error(self, error: Exception) -> None:
        """Handle error with registered handlers.

        Record the error in statistics and call all registered error handlers.
        Errors in handlers are caught and logged but don't stop the process.

        Parameters
        ----------
        error : Exception
            The error to handle.
        """
        self._last_error = error
        self._stats["error_count"] += 1
        self._stats["last_error"] = datetime.now()

        for handler in self._error_handlers:
            try:
                handler(error)
            except Exception as e:
                logger.error(f"Error in error handler: {e}")

    def get_stats(self) -> dict[str, Any]:
        """Get module statistics.

        Returns a copy of the module's internal statistics.

        Returns
        -------
        dict[str, Any]
            Dictionary containing module statistics:
            - fetch_count: Number of successful fetch operations
            - error_count: Number of errors encountered
            - last_fetch: Timestamp of last successful fetch
            - last_error: Timestamp of last error
        """
        return self._stats.copy()

    def reset_stats(self) -> None:
        """Reset module statistics.

        Reset all statistics counters to their initial values.
        """
        self._stats = {
            "fetch_count": 0,
            "error_count": 0,
            "last_fetch": None,
            "last_error": None,
        }

    async def async_fetch(self) -> list[dict[str, Any]]:
        """Async version of fetch method.

        Asynchronous version of the fetch method that can be used
        in async contexts.

        Returns
        -------
        list[dict[str, Any]]
            List of items returned by the fetch method.
        """
        return self.fetch()

    def fetch_with_retry(
        self, max_retries: int = 3, retry_delay: float = 1.0
    ) -> list[dict[str, Any]]:
        """Fetch data with retry logic.

        Attempt to fetch data with automatic retries on failure.

        Parameters
        ----------
        max_retries : int, default=3
            Maximum number of retry attempts.
        retry_delay : float, default=1.0
            Delay in seconds between retry attempts.

        Returns
        -------
        list[dict[str, Any]]
            List of items returned by the fetch method.

        Raises
        ------
        Exception
            If all retry attempts fail, the last exception is raised.
        """
        for attempt in range(max_retries):
            try:
                result = self.fetch()
                self._stats["fetch_count"] += 1
                self._stats["last_fetch"] = datetime.now()
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    self._handle_error(e)
                    raise
                logger.warning(f"Fetch attempt {attempt + 1} failed, retrying...")
                import time

                time.sleep(retry_delay)

        return []

    def initialize(self) -> None:
        """Initialize the module.

        Perform one-time initialization of the module. This method
        ensures initialization only happens once.
        """
        if not self._is_initialized:
            try:
                self._initialize_module()
                self._is_initialized = True
                logger.info(f"Module {self.id} initialized successfully")
            except Exception as e:
                self._handle_error(e)
                logger.error(f"Failed to initialize module {self.id}: {e}")
                raise

    def _initialize_module(self) -> None:
        """Initialize module-specific resources.

        Override this method to perform module-specific initialization.
        Called once during the first call to initialize().
        """
        pass

    def shutdown(self) -> None:
        """Shutdown the module.

        Perform cleanup operations when the module is being shut down.
        """
        try:
            self._shutdown_module()
            self.cleanup()
            logger.info(f"Module {self.id} shutdown successfully")
        except Exception as e:
            logger.error(f"Error shutting down module {self.id}: {e}")

    def _shutdown_module(self) -> None:
        """Shutdown module-specific resources.

        Override this method to perform module-specific cleanup.
        Called by shutdown().
        """
        pass

    def export_data(self, format: str = "json") -> Any:
        """Export module data in specified format.

        Export the current module data in the specified format.

        Parameters
        ----------
        format : str, default="json"
            Export format. Supported formats: "json", "csv".

        Returns
        -------
        Any
            Exported data in the specified format.

        Raises
        ------
        ValueError
            If an unsupported format is specified.
        """
        data = self.fetch()

        if format == "json":
            import json

            return json.dumps(data, indent=2, ensure_ascii=False)
        elif format == "csv":
            import csv
            import io

            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def import_data(self, data: Any, format: str = "json") -> bool:
        """Import module data from specified format.

        Import data into the module from the specified format.

        Parameters
        ----------
        data : Any
            Data to import.
        format : str, default="json"
            Import format. Currently only "json" is supported.

        Returns
        -------
        bool
            True if import was successful, False otherwise.
        """
        try:
            if format == "json":
                import json

                parsed_data = json.loads(data)
                self._process_imported_data(parsed_data)
                return True
            else:
                raise ValueError(f"Unsupported import format: {format}")
        except Exception as e:
            logger.error(f"Failed to import data: {e}")
            return False

    def _process_imported_data(self, data: Any) -> None:
        """Process imported data.

        Override this method to handle imported data in a
        module-specific way.

        Parameters
        ----------
        data : Any
            Parsed data to process.
        """
        pass

    def render_config_ui(self) -> None:
        """Render configuration UI for the module.

        Render UI components for configuring the module. Uses
        the configuration schema to automatically generate
        appropriate input elements.
        """
        schema = self.get_config_schema()
        if not schema:
            ui.label("No configuration available").classes("text-gray-500")
            return

        with ui.card().classes("w-full p-4"):
            ui.label("Module Configuration").classes("text-lg font-semibold mb-4")

            # Render configuration fields based on schema
            for field_name, field_config in schema.items():
                field_type = field_config.get("type", "string")
                field_label = field_config.get("label", field_name)
                field_default = field_config.get("default", "")
                field_description = field_config.get("description", "")

                with ui.column().classes("w-full gap-2 mb-4"):
                    ui.label(field_label).classes("text-sm font-medium")
                    if field_description:
                        ui.label(field_description).classes("text-xs text-gray-500")

                    if field_type == "string":
                        ui.input(
                            placeholder=field_label,
                            value=self.config.get(field_name, field_default),
                        ).classes("w-full").bind_value(self.config, field_name)
                    elif field_type == "number":
                        ui.number(
                            label=field_label,
                            value=self.config.get(field_name, field_default),
                        ).classes("w-full").bind_value(self.config, field_name)
                    elif field_type == "boolean":
                        ui.switch(
                            text=field_label,
                            value=self.config.get(field_name, field_default),
                        ).bind_value(self.config, field_name)
                    elif field_type == "select":
                        options = field_config.get("options", [])
                        ui.select(
                            options=options,
                            label=field_label,
                            value=self.config.get(field_name, field_default),
                        ).classes("w-full").bind_value(self.config, field_name)

    def render_stats_ui(self) -> None:
        """Render statistics UI for the module.

        Render UI components for displaying module statistics
        including fetch counts, error counts, and timestamps.
        """
        stats = self.get_stats()

        with ui.card().classes("w-full p-4"):
            ui.label("Module Statistics").classes("text-lg font-semibold mb-4")

            with ui.column().classes("w-full gap-2"):
                ui.label(f"Fetch Count: {stats['fetch_count']}").classes("text-sm")
                ui.label(f"Error Count: {stats['error_count']}").classes("text-sm")

                if stats["last_fetch"]:
                    ui.label(
                        f"Last Fetch: {stats['last_fetch'].strftime('%Y-%m-%d %H:%M:%S')}"
                    ).classes("text-sm")

                if stats["last_error"]:
                    ui.label(
                        f"Last Error: {stats['last_error'].strftime('%Y-%m-%d %H:%M:%S')}"
                    ).classes("text-sm")

                if self._last_error:
                    ui.label(f"Error: {str(self._last_error)}").classes(
                        "text-sm text-red-600"
                    )

    def render_action_buttons(self) -> None:
        """Render action buttons for the module.

        Render UI components for common module actions such as
        refresh, export, and data clearing.
        """
        with ui.row().classes("w-full gap-2"):
            ui.button("Refresh", icon="refresh", on_click=self._manual_refresh).classes(
                "bg-blue-500 text-white"
            )

            ui.button("Export", icon="download", on_click=self._export_data).classes(
                "bg-green-500 text-white"
            )

            if self.has_persistence():
                ui.button(
                    "Clear Data", icon="delete", on_click=self._clear_data
                ).classes("bg-red-500 text-white")

    def _manual_refresh(self) -> None:
        """Manual refresh handler.

        Handle manual refresh requests from the UI.
        """
        try:
            self.fetch()
            self._notify_refresh()
            ui.notify("Data refreshed successfully", type="positive")
        except Exception as e:
            self._handle_error(e)
            ui.notify(f"Failed to refresh: {str(e)}", type="negative")

    def _export_data(self) -> None:
        """Export data handler.

        Handle data export requests from the UI.
        """
        try:
            data = self.export_data()
            # Create download link
            ui.download(
                data,
                filename=f"{self.id}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            )
            ui.notify("Data exported successfully", type="positive")
        except Exception as e:
            self._handle_error(e)
            ui.notify(f"Failed to export: {str(e)}", type="negative")

    def _clear_data(self) -> None:
        """Clear data handler.

        Handle data clearing requests from the UI.
        """
        try:
            storage = self.get_storage()
            storage.clear()
            cache = self.get_cache()
            cache.clear()
            ui.notify("Data cleared successfully", type="positive")
        except Exception as e:
            self._handle_error(e)
            ui.notify(f"Failed to clear data: {str(e)}", type="negative")
