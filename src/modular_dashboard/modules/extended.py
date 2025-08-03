"""Extended module base class with extended functionality."""

from collections.abc import Callable
from datetime import datetime
from typing import Any

from loguru import logger
from nicegui import ui

from .base import Module


class ExtendedModule(Module):
    """Extended module with extended functionality."""

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
        """Module version."""
        return "1.0.0"

    @property
    def category(self) -> str:
        """Module category."""
        return "general"

    @property
    def supported_features(self) -> list[str]:
        """List of supported features."""
        return []

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration for the module."""
        return {}

    def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate module configuration."""
        return True

    def get_config_schema(self) -> dict[str, Any]:
        """Get configuration schema for UI generation."""
        return {}

    def add_refresh_callback(self, callback: Callable) -> None:
        """Add a callback to be called when data is refreshed."""
        self._refresh_callbacks.append(callback)

    def add_error_handler(self, handler: Callable) -> None:
        """Add an error handler."""
        self._error_handlers.append(handler)

    def _notify_refresh(self) -> None:
        """Notify all refresh callbacks."""
        for callback in self._refresh_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in refresh callback: {e}")

    def _handle_error(self, error: Exception) -> None:
        """Handle error with registered handlers."""
        self._last_error = error
        self._stats["error_count"] += 1
        self._stats["last_error"] = datetime.now()

        for handler in self._error_handlers:
            try:
                handler(error)
            except Exception as e:
                logger.error(f"Error in error handler: {e}")

    def get_stats(self) -> dict[str, Any]:
        """Get module statistics."""
        return self._stats.copy()

    def reset_stats(self) -> None:
        """Reset module statistics."""
        self._stats = {
            "fetch_count": 0,
            "error_count": 0,
            "last_fetch": None,
            "last_error": None,
        }

    async def async_fetch(self) -> list[dict[str, Any]]:
        """Async version of fetch method."""
        return self.fetch()

    def fetch_with_retry(
        self, max_retries: int = 3, retry_delay: float = 1.0
    ) -> list[dict[str, Any]]:
        """Fetch data with retry logic."""
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
        """Initialize the module."""
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
        """Initialize module-specific resources."""
        pass

    def shutdown(self) -> None:
        """Shutdown the module."""
        try:
            self._shutdown_module()
            self.cleanup()
            logger.info(f"Module {self.id} shutdown successfully")
        except Exception as e:
            logger.error(f"Error shutting down module {self.id}: {e}")

    def _shutdown_module(self) -> None:
        """Shutdown module-specific resources."""
        pass

    def export_data(self, format: str = "json") -> Any:
        """Export module data in specified format."""
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
        """Import module data from specified format."""
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
        """Process imported data."""
        pass

    def render_config_ui(self) -> None:
        """Render configuration UI for the module."""
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
        """Render statistics UI for the module."""
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
        """Render action buttons for the module."""
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
        """Manual refresh handler."""
        try:
            self.fetch()
            self._notify_refresh()
            ui.notify("Data refreshed successfully", type="positive")
        except Exception as e:
            self._handle_error(e)
            ui.notify(f"Failed to refresh: {str(e)}", type="negative")

    def _export_data(self) -> None:
        """Export data handler."""
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
        """Clear data handler."""
        try:
            storage = self.get_storage()
            storage.clear()
            cache = self.get_cache()
            cache.clear()
            ui.notify("Data cleared successfully", type="positive")
        except Exception as e:
            self._handle_error(e)
            ui.notify(f"Failed to clear data: {str(e)}", type="negative")
