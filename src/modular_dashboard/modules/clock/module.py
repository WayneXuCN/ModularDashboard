"""Clock module for displaying current time and date."""

import asyncio
from datetime import datetime
from typing import Any

from nicegui import ui

from ..extended import ExtendedModule


class ClockModule(ExtendedModule):
    """Clock module for displaying current time and date."""

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.time_label = None
        self.date_label = None
        self.timezone = self.config.get("timezone", "local")
        self.format_24h = self.config.get("format_24h", False)
        self.show_seconds = self.config.get("show_seconds", True)
        self.update_interval = self.config.get("update_interval", 1)

    @property
    def id(self) -> str:
        return "clock"

    @property
    def name(self) -> str:
        return "Clock"

    @property
    def icon(self) -> str:
        return "schedule"

    @property
    def description(self) -> str:
        return "Display current time and date"

    @property
    def version(self) -> str:
        return "1.0.0"

    def _get_current_time(self) -> datetime:
        """Get current time based on timezone setting."""
        if self.timezone == "utc":
            return datetime.utcnow()
        else:
            return datetime.now()

    def _format_time(self, dt: datetime) -> str:
        """Format time according to settings."""
        if self.format_24h:
            time_format = "%H:%M"
            if self.show_seconds:
                time_format = "%H:%M:%S"
        else:
            time_format = "%I:%M"
            if self.show_seconds:
                time_format = "%I:%M:%S"

        time_str = dt.strftime(time_format)
        if not self.format_24h:
            time_str += dt.strftime(" %p")

        return time_str

    def _format_date(self, dt: datetime) -> str:
        """Format date according to settings."""
        date_format = self.config.get("date_format", "%A, %B %d, %Y")
        return dt.strftime(date_format)

    async def _update_clock(self) -> None:
        """Update the clock display."""
        while True:
            try:
                if self.time_label and hasattr(self.time_label, 'client') and self.time_label.client and self.date_label and hasattr(self.date_label, 'client') and self.date_label.client:
                    now = self._get_current_time()
                    self.time_label.text = self._format_time(now)
                    self.date_label.text = self._format_date(now)
            except (RuntimeError, AttributeError):
                # Client disconnected, stop updating
                break
            await asyncio.sleep(self.update_interval)

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch current time data."""
        now = self._get_current_time()
        return [
            {
                "title": "Current Time",
                "summary": f"{self._format_time(now)} - {self._format_date(now)}",
                "link": "",
                "published": now.isoformat(),
                "tags": ["time", "clock"],
                "extra": {
                    "time": self._format_time(now),
                    "date": self._format_date(now),
                    "timezone": self.timezone,
                    "format_24h": self.format_24h,
                    "show_seconds": self.show_seconds,
                },
            }
        ]

    def render(self) -> None:
        """Render the clock module UI."""
        now = self._get_current_time()

        with ui.column().classes("w-full items-center justify-center gap-2"):
            # Time display
            self.time_label = ui.label(self._format_time(now)).classes(
                "text-4xl font-bold text-blue-600 tabular-nums"
            )

            # Date display
            self.date_label = ui.label(self._format_date(now)).classes(
                "text-lg text-gray-600 text-center"
            )

            # Start the clock update loop
            ui.timer(self.update_interval, self._update_clock)

    def render_detail(self) -> None:
        """Render detailed clock view."""
        now = self._get_current_time()

        with ui.column().classes("w-full gap-8 max-w-2xl mx-auto items-center"):
            ui.label("World Clock").classes("text-3xl font-bold text-center")

            # Main clock display
            with ui.card().classes("w-full p-8 text-center"):
                self.time_label = ui.label(self._format_time(now)).classes(
                    "text-6xl font-bold text-blue-600 tabular-nums"
                )

                self.date_label = ui.label(self._format_date(now)).classes(
                    "text-2xl text-gray-600 mt-4"
                )

            # Time zone info
            with (
                ui.card().classes("w-full p-4 text-center"),
                ui.row().classes("w-full justify-center gap-4 text-sm"),
            ):
                ui.label(f"Timezone: {self.timezone.upper()}")
                ui.label(f"Format: {'24-hour' if self.format_24h else '12-hour'}")
                if self.show_seconds:
                    ui.label("Show: Seconds")

            # Additional time zones
            ui.label("Other Time Zones").classes("text-xl font-semibold mt-4")

            with ui.row().classes("w-full gap-4 justify-center"):
                # Local time
                local_time = datetime.now()
                with ui.card().classes("p-4 text-center min-w-[150px]"):
                    ui.label("Local").classes("font-semibold text-gray-600")
                    ui.label(local_time.strftime("%H:%M")).classes("text-2xl font-bold")
                    ui.label(local_time.strftime("%Y-%m-%d")).classes(
                        "text-sm text-gray-500"
                    )

                # UTC time
                utc_time = datetime.utcnow()
                with ui.card().classes("p-4 text-center min-w-[150px]"):
                    ui.label("UTC").classes("font-semibold text-gray-600")
                    ui.label(utc_time.strftime("%H:%M")).classes("text-2xl font-bold")
                    ui.label(utc_time.strftime("%Y-%m-%d")).classes(
                        "text-sm text-gray-500"
                    )

            # Start the clock update loop
            ui.timer(self.update_interval, self._update_clock)
