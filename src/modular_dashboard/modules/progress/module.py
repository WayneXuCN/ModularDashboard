"""Progress module for time progress tracking."""

import asyncio
from datetime import datetime
from typing import Any

from nicegui import ui

from ...ui.styles import DashboardStyles
from ..extended import ExtendedModule


class ProgressModule(ExtendedModule):
    """Progress module for time progress tracking."""

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.selected_period = self.config.get("default_period", "day")
        self.auto_update = self.config.get("auto_update", True)
        self.update_interval = self.config.get("update_interval", 60)  # seconds
        self.progress_bars = {}
        self.progress_labels = {}
        self.main_progress_label = None
        self.main_progress_value = None
        self.main_progress_bar = None
        self.main_date_label = None
        self.overview_cards = {}

    @property
    def id(self) -> str:
        return "progress"

    @property
    def name(self) -> str:
        return "Time Progress"

    @property
    def icon(self) -> str:
        return "timeline"

    @property
    def description(self) -> str:
        return "Visualize time progress for day, month, and year"

    @property
    def version(self) -> str:
        return "1.0.0"

    def _calculate_progress(self, period: str) -> tuple[float, str]:
        """Calculate progress percentage and label for a given period."""
        now = datetime.now()

        if period == "day":
            total_seconds = 24 * 60 * 60
            elapsed_seconds = now.hour * 3600 + now.minute * 60 + now.second
            label = f"Day Progress ({now.strftime('%Y-%m-%d')})"
        elif period == "month":
            days_in_month = (
                now.replace(month=now.month % 12 + 1, day=1) - now.replace(day=1)
            ).days
            total_seconds = days_in_month * 24 * 60 * 60
            elapsed_seconds = (
                (now.day - 1) * 24 * 60 * 60
                + now.hour * 3600
                + now.minute * 60
                + now.second
            )
            label = f"Month Progress ({now.strftime('%B %Y')})"
        elif period == "year":
            is_leap = now.year % 4 == 0 and (now.year % 100 != 0 or now.year % 400 == 0)
            days_in_year = 366 if is_leap else 365
            total_seconds = days_in_year * 24 * 60 * 60
            elapsed_seconds = (
                (now.timetuple().tm_yday - 1) * 24 * 60 * 60
                + now.hour * 3600
                + now.minute * 60
                + now.second
            )
            label = f"Year Progress ({now.year})"
        else:
            return 0.0, "Unknown Period"

        progress = min(100.0, (elapsed_seconds / total_seconds) * 100)
        return progress, label

    async def _update_progress(self) -> None:
        """Update progress bars with current values."""
        while True:
            try:
                if self.auto_update:
                    # Update main progress display
                    progress, label = self._calculate_progress(self.selected_period)

                    if (
                        self.main_progress_value
                        and hasattr(self.main_progress_value, "client")
                        and self.main_progress_value.client
                    ):
                        self.main_progress_value.text = f"{progress:.1f}%"
                    if (
                        self.main_progress_bar
                        and hasattr(self.main_progress_bar, "client")
                        and self.main_progress_bar.client
                    ):
                        self.main_progress_bar.value = progress / 100
                    if (
                        self.main_progress_label
                        and hasattr(self.main_progress_label, "client")
                        and self.main_progress_label.client
                    ):
                        period_labels = {
                            "day": "Today",
                            "month": "This Month",
                            "year": "This Year",
                        }
                        self.main_progress_label.text = period_labels.get(
                            self.selected_period, "Progress"
                        )
                    if (
                        self.main_date_label
                        and hasattr(self.main_date_label, "client")
                        and self.main_date_label.client
                    ):
                        # Extract just the date part from the full label
                        date_part = (
                            label.split(" (")[1].rstrip(")") if " (" in label else label
                        )
                        self.main_date_label.text = date_part

                    # Update individual progress displays
                    for period in ["day", "month", "year"]:
                        progress, label = self._calculate_progress(period)
                        if (
                            period in self.progress_bars
                            and hasattr(self.progress_bars[period], "client")
                            and self.progress_bars[period].client
                        ):
                            self.progress_bars[period].value = progress / 100
                        if (
                            period in self.progress_labels
                            and hasattr(self.progress_labels[period], "client")
                            and self.progress_labels[period].client
                        ):
                            self.progress_labels[period].text = f"{progress:.1f}%"
            except (RuntimeError, AttributeError):
                # Client disconnected, stop updating
                break
            await asyncio.sleep(self.update_interval)

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch progress data."""
        items = []
        periods = ["day", "month", "year"]

        for period in periods:
            progress, label = self._calculate_progress(period)
            items.append(
                {
                    "title": label,
                    "summary": f"{progress:.2f}% complete",
                    "link": "",
                    "published": datetime.now().isoformat(),
                    "tags": ["progress", period],
                    "extra": {"period": period, "progress": progress, "label": label},
                }
            )

        return items

    def render(self) -> None:
        """Render the progress module UI."""
        with ui.column().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.GAP_MD}"
        ):
            # Period selection with Apple-style design
            with ui.row().classes(
                f"{DashboardStyles.FULL_WIDTH} justify-center {DashboardStyles.GAP_SM}"
            ):
                period_labels = {"day": "Today", "month": "Month", "year": "Year"}

                for period, label in period_labels.items():
                    btn = ui.button(
                        label, on_click=lambda e, p=period: self._select_period(p)
                    ).classes(
                        "px-4 py-2 rounded-full text-sm font-medium transition-all"
                    )
                    # Store button reference for styling updates
                    if not hasattr(self, "period_buttons"):
                        self.period_buttons = {}
                    self.period_buttons[period] = btn

                # Set initial button style
                self._update_button_styles()

            # Main progress display with modern styling
            with ui.card().classes(
                f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_XL} rounded-2xl shadow-md"
            ):
                # Period label
                self.main_progress_label = ui.label("Today").classes(
                    DashboardStyles.TITLE_H3 + " text-center"
                )

                # Large progress percentage
                progress, label = self._calculate_progress(self.selected_period)
                self.main_progress_value = ui.label(f"{progress:.1f}%").classes(
                    DashboardStyles.TITLE_H1 + " text-center my-2"
                )

                # Progress bar with rounded corners
                self.main_progress_bar = ui.linear_progress(
                    value=progress / 100, show_value=False
                ).classes("w-full h-4 rounded-full")

                # Date label
                date_part = label.split(" (")[1].rstrip(")") if " (" in label else label
                self.main_date_label = ui.label(date_part).classes(
                    DashboardStyles.SUBTLE_TEXT + " text-center mt-2"
                )

            # Start the update loop
            ui.timer(self.update_interval, self._update_progress)

    def _select_period(self, period: str) -> None:
        """Handle period selection."""
        self.selected_period = period
        # Update button styles based on which view we're in
        if hasattr(self, "period_buttons"):
            self._update_button_styles()
        elif hasattr(self, "detail_period_buttons"):
            self._update_detail_button_styles()
        # Force immediate update
        asyncio.create_task(self._update_progress_single())

    def _update_button_styles(self) -> None:
        """Update period button styles based on selection."""
        for p, btn in self.period_buttons.items():
            if p == self.selected_period:
                btn.classes(
                    replace="px-4 py-2 rounded-full text-sm font-medium transition-all bg-blue-500 text-white"
                )
            else:
                btn.classes(
                    replace="px-4 py-2 rounded-full text-sm font-medium transition-all bg-gray-100 text-gray-700 hover:bg-gray-200"
                )

    async def _update_progress_single(self) -> None:
        """Update progress display once."""
        try:
            progress, label = self._calculate_progress(self.selected_period)

            if (
                self.main_progress_value
                and hasattr(self.main_progress_value, "client")
                and self.main_progress_value.client
            ):
                self.main_progress_value.text = f"{progress:.1f}%"
            if (
                self.main_progress_bar
                and hasattr(self.main_progress_bar, "client")
                and self.main_progress_bar.client
            ):
                self.main_progress_bar.value = progress / 100
            if (
                self.main_progress_label
                and hasattr(self.main_progress_label, "client")
                and self.main_progress_label.client
            ):
                period_labels = {
                    "day": "Today",
                    "month": "This Month",
                    "year": "This Year",
                }
                self.main_progress_label.text = period_labels.get(
                    self.selected_period, "Progress"
                )
            if (
                self.main_date_label
                and hasattr(self.main_date_label, "client")
                and self.main_date_label.client
            ):
                date_part = label.split(" (")[1].rstrip(")") if " (" in label else label
                self.main_date_label.text = date_part
        except (RuntimeError, AttributeError):
            # Client disconnected, ignore
            pass

    def render_detail(self) -> None:
        """Render detailed progress view."""
        with ui.column().classes("w-full gap-6 max-w-2xl mx-auto"):
            ui.label("Time Progress Tracker").classes(
                DashboardStyles.TITLE_H1 + " " + DashboardStyles.TEXT_CENTER
            )

            # Explanation
            ui.markdown("""
            This module visualizes how much time has passed in the current day, month, and year.
            Use the buttons to switch between different time periods.
            """).classes(DashboardStyles.TEXT_CENTER + " " + DashboardStyles.TEXT_MUTED)

            # Period selection with larger buttons
            with ui.row().classes("w-full justify-center gap-3 my-6"):
                period_labels = {
                    "day": "Today",
                    "month": "This Month",
                    "year": "This Year",
                }

                for period, label in period_labels.items():
                    btn = ui.button(
                        label, on_click=lambda e, p=period: self._select_period(p)
                    ).classes(
                        "px-6 py-3 rounded-full text-base font-medium transition-all"
                    )
                    # Store button reference for styling updates
                    if not hasattr(self, "detail_period_buttons"):
                        self.detail_period_buttons = {}
                    self.detail_period_buttons[period] = btn

                # Set initial button style
                self._update_detail_button_styles()

            # Main progress display
            with ui.card().classes("w-full p-8 rounded-2xl shadow-lg"):
                # Large progress percentage
                progress, label = self._calculate_progress(self.selected_period)

                period_labels = {
                    "day": "Today",
                    "month": "This Month",
                    "year": "This Year",
                }

                ui.label(period_labels.get(self.selected_period, "Progress")).classes(
                    DashboardStyles.TITLE_H2 + " " + DashboardStyles.TEXT_CENTER
                )
                self.main_progress_value = ui.label(f"{progress:.1f}%").classes(
                    DashboardStyles.TITLE_H1 + " text-blue-600 text-center my-4"
                )

                # Progress bar
                self.main_progress_bar = ui.linear_progress(
                    value=progress / 100, show_value=False
                ).classes("w-full h-6 rounded-full")

                # Date label
                date_part = label.split(" (")[1].rstrip(")") if " (" in label else label
                self.main_date_label = ui.label(date_part).classes(
                    DashboardStyles.BODY_TEXT
                    + " "
                    + DashboardStyles.TEXT_CENTER
                    + " mt-2"
                )

            # Start the update loop
            ui.timer(self.update_interval, self._update_progress)

    def _update_detail_button_styles(self) -> None:
        """Update period button styles for detailed view."""
        for p, btn in self.detail_period_buttons.items():
            if p == self.selected_period:
                btn.classes(
                    replace="px-6 py-3 rounded-full text-base font-medium transition-all bg-blue-500 text-white"
                )
            else:
                btn.classes(
                    replace="px-6 py-3 rounded-full text-base font-medium transition-all bg-gray-100 text-gray-700 hover:bg-gray-200"
                )
