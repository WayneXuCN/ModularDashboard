"""Weather module for displaying current weather information."""

import json
from datetime import datetime
from typing import Any
from urllib.request import urlopen

from nicegui import ui

from ..extended import ExtendedModule


class WeatherModule(ExtendedModule):
    """Weather module for displaying current weather information."""

    @property
    def id(self) -> str:
        return "weather"

    @property
    def name(self) -> str:
        return "Weather"

    @property
    def icon(self) -> str:
        return "wb_sunny"

    @property
    def description(self) -> str:
        return "Display current weather information"

    @property
    def version(self) -> str:
        return "1.0.0"

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch weather data from OpenWeatherMap API."""
        api_key = self.config.get("api_key")
        city = self.config.get("city", "Beijing")

        if not api_key:
            # Return mock data if no API key
            return [
                {
                    "title": f"Weather in {city}",
                    "summary": "Mock weather data - Please configure API key",
                    "link": "https://openweathermap.org/",
                    "published": datetime.now().isoformat(),
                    "tags": ["weather", "mock"],
                    "extra": {
                        "temperature": "22°C",
                        "humidity": "65%",
                        "wind_speed": "3.5 m/s",
                        "condition": "Partly cloudy",
                    },
                }
            ]

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            with urlopen(url) as response:
                data = json.loads(response.read().decode())

            return [
                {
                    "title": f"Weather in {data['name']}",
                    "summary": data["weather"][0]["description"].title(),
                    "link": "https://openweathermap.org/",
                    "published": datetime.now().isoformat(),
                    "tags": ["weather", "current"],
                    "extra": {
                        "temperature": f"{data['main']['temp']}°C",
                        "humidity": f"{data['main']['humidity']}%",
                        "wind_speed": f"{data['wind']['speed']} m/s",
                        "condition": data["weather"][0]["description"].title(),
                        "feels_like": f"{data['main']['feels_like']}°C",
                    },
                }
            ]
        except Exception as e:
            return [
                {
                    "title": "Weather Error",
                    "summary": f"Failed to fetch weather data: {str(e)}",
                    "link": "https://openweathermap.org/",
                    "published": datetime.now().isoformat(),
                    "tags": ["weather", "error"],
                    "extra": {},
                }
            ]

    def render(self) -> None:
        """Render the weather module UI."""
        data = self.fetch()
        if not data:
            ui.label("No weather data available").classes("text-gray-500")
            return

        weather = data[0]
        extra = weather.get("extra", {})

        with ui.column().classes("w-full gap-2"):
            # Location and condition
            with ui.row().classes("w-full justify-between items-center"):
                ui.label(weather["title"]).classes("text-lg font-semibold")
                ui.label(extra.get("condition", "")).classes("text-sm text-gray-600")

            # Temperature
            if extra.get("temperature"):
                ui.label(extra["temperature"]).classes(
                    "text-3xl font-bold text-blue-600"
                )

            # Additional info
            with ui.row().classes("w-full gap-4 text-sm"):
                if extra.get("feels_like"):
                    ui.label(f"Feels like: {extra['feels_like']}").classes(
                        "text-gray-600"
                    )
                if extra.get("humidity"):
                    ui.label(f"Humidity: {extra['humidity']}").classes("text-gray-600")
                if extra.get("wind_speed"):
                    ui.label(f"Wind: {extra['wind_speed']}").classes("text-gray-600")

    def render_detail(self) -> None:
        """Render detailed weather view."""
        data = self.fetch()
        if not data:
            ui.label("No weather data available").classes(
                "text-gray-500 text-center w-full"
            )
            return

        weather = data[0]
        extra = weather.get("extra", {})

        with ui.column().classes("w-full gap-6 max-w-2xl mx-auto"):
            ui.label("Current Weather").classes("text-3xl font-bold text-center")

            # Main weather card
            with (
                ui.card().classes("w-full p-6"),
                ui.column().classes("w-full gap-4 items-center"),
            ):
                # Location
                ui.label(weather["title"]).classes("text-2xl font-semibold")

                # Temperature
                if extra.get("temperature"):
                    ui.label(extra["temperature"]).classes(
                        "text-5xl font-bold text-blue-600"
                    )

                # Condition
                if extra.get("condition"):
                    ui.label(extra["condition"]).classes("text-xl text-gray-600")

                # Additional details
                with ui.row().classes("w-full justify-center gap-6 text-sm"):
                    if extra.get("feels_like"):
                        ui.label(f"Feels like: {extra['feels_like']}").classes(
                            "text-gray-600"
                        )
                    if extra.get("humidity"):
                        ui.label(f"Humidity: {extra['humidity']}").classes(
                            "text-gray-600"
                        )
                    if extra.get("wind_speed"):
                        ui.label(f"Wind: {extra['wind_speed']}").classes(
                            "text-gray-600"
                        )

            # Configuration info
            if not self.config.get("api_key"):
                ui.label(
                    "💡 Configure OpenWeatherMap API key for real weather data"
                ).classes("text-sm text-gray-500 text-center")
