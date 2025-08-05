"""Weather module for displaying current weather information with hourly forecast."""

import json
from datetime import datetime
from typing import Any
from urllib.request import urlopen

from nicegui import ui

from ...ui.styles import DashboardStyles
from ..extended import ExtendedModule


class WeatherModule(ExtendedModule):
    """Weather module for displaying current weather information with hourly forecast."""

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
        return "Display current weather information with hourly forecast"

    @property
    def version(self) -> str:
        return "2.0.0"

    @property
    def category(self) -> str:
        return "utility"

    @property
    def supported_features(self) -> list[str]:
        return ["hourly_forecast", "temperature_scale", "location_display"]

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration for the weather module."""
        return {
            "api_key": "",
            "city": "Beijing",
            "units": "metric",
            "hide_location": False,
            "show_area_name": True,
            "hours_to_show": 12,
        }

    def get_config_schema(self) -> dict[str, Any]:
        """Get configuration schema for UI generation."""
        return {
            "api_key": {
                "type": "string",
                "label": "OpenWeatherMap API Key",
                "description": "Your OpenWeatherMap API key for fetching weather data",
                "default": "",
            },
            "city": {
                "type": "string",
                "label": "City",
                "description": "City name for weather data",
                "default": "Beijing",
            },
            "units": {
                "type": "select",
                "label": "Units",
                "description": "Temperature units (metric/imperial)",
                "default": "metric",
                "options": [
                    {"label": "Celsius", "value": "metric"},
                    {"label": "Fahrenheit", "value": "imperial"},
                ],
            },
            "hide_location": {
                "type": "boolean",
                "label": "Hide Location",
                "description": "Hide location display in widget",
                "default": False,
            },
            "show_area_name": {
                "type": "boolean",
                "label": "Show Area Name",
                "description": "Include area name in location display",
                "default": True,
            },
            "hours_to_show": {
                "type": "number",
                "label": "Hours to Show",
                "description": "Number of hours to display in forecast",
                "default": 12,
                "min": 6,
                "max": 24,
            },
        }

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch weather data from OpenWeatherMap API with hourly forecast."""
        api_key = self.config.get("api_key")
        city = self.config.get("city", "Beijing")
        units = self.config.get("units", "metric")
        hours_to_show = self.config.get("hours_to_show", 12)

        if not api_key:
            # Return mock data if no API key
            return self._get_mock_data(city, units, hours_to_show)

        try:
            # Fetch current weather and forecast
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}&cnt={hours_to_show + 1}"

            with urlopen(current_url) as response:
                current_data = json.loads(response.read().decode())

            with urlopen(forecast_url) as response:
                forecast_data = json.loads(response.read().decode())

            return self._process_weather_data(
                current_data, forecast_data, units, hours_to_show
            )
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

    def _get_mock_data(
        self, city: str, units: str, hours_to_show: int
    ) -> list[dict[str, Any]]:
        """Get mock weather data for testing."""
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"

        # Generate hourly forecast data
        columns = []
        current_hour = datetime.now().hour
        temps = [22, 23, 24, 25, 26, 25, 24, 23, 22, 21, 20, 19]

        for i in range(hours_to_show):
            hour = (current_hour + i) % 24
            temp = temps[i % len(temps)]
            columns.append(
                {
                    "time": f"{hour:02d}:00",
                    "temperature": temp,
                    "scale": (temp - 10) / 30,  # Normalize to 0-1 range
                    "has_precipitation": i in [3, 4, 10],
                    "is_current": i == 0,
                }
            )

        return [
            {
                "title": f"Weather in {city}",
                "summary": "Mock weather data - Please configure API key",
                "link": "https://openweathermap.org/",
                "published": datetime.now().isoformat(),
                "tags": ["weather", "mock"],
                "extra": {
                    "temperature": f"22{temp_unit}",
                    "humidity": "65%",
                    "wind_speed": f"3.5 {speed_unit}",
                    "condition": "Partly cloudy",
                    "feels_like": f"23{temp_unit}",
                    "weather_code": "partly_cloudy",
                    "apparent_temperature": 23,
                    "columns": columns,
                    "current_column": 0,
                    "sunrise_column": 2,
                    "sunset_column": 8,
                    "place": {
                        "name": city,
                        "area": "",
                        "country": "Mock Country",
                    },
                    "units": units,
                    "hide_location": self.config.get("hide_location", False),
                    "show_area_name": self.config.get("show_area_name", True),
                },
            }
        ]

    def _process_weather_data(
        self, current_data: dict, forecast_data: dict, units: str, hours_to_show: int
    ) -> list[dict[str, Any]]:
        """Process weather data from API responses."""
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"

        # Process hourly forecast
        columns = []
        current_hour = datetime.now().hour
        temp_range = [
            item["main"]["temp"] for item in forecast_data["list"][:hours_to_show]
        ]
        min_temp = min(temp_range)
        max_temp = max(temp_range)
        temp_range_size = max_temp - min_temp if max_temp != min_temp else 1

        for i, item in enumerate(forecast_data["list"][:hours_to_show]):
            temp = item["main"]["temp"]
            columns.append(
                {
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%H:00"),
                    "temperature": int(round(temp)),
                    "scale": (temp - min_temp) / temp_range_size
                    if temp_range_size > 0
                    else 0.5,
                    "has_precipitation": item.get("rain", {}).get("3h", 0) > 0
                    or item.get("snow", {}).get("3h", 0) > 0,
                    "is_current": i == 0,
                }
            )

        # Calculate sunrise/sunset columns
        sunrise_time = datetime.fromtimestamp(current_data["sys"]["sunrise"]).hour
        sunset_time = datetime.fromtimestamp(current_data["sys"]["sunset"]).hour
        sunrise_column = max(0, min(len(columns) - 1, sunrise_time - current_hour))
        sunset_column = max(0, min(len(columns) - 1, sunset_time - current_hour))

        return [
            {
                "title": f"Weather in {current_data['name']}",
                "summary": current_data["weather"][0]["description"].title(),
                "link": "https://openweathermap.org/",
                "published": datetime.now().isoformat(),
                "tags": ["weather", "current"],
                "extra": {
                    "temperature": f"{int(round(current_data['main']['temp']))}{temp_unit}",
                    "humidity": f"{current_data['main']['humidity']}%",
                    "wind_speed": f"{current_data['wind']['speed']} {speed_unit}",
                    "condition": current_data["weather"][0]["description"].title(),
                    "feels_like": f"{int(round(current_data['main']['feels_like']))}{temp_unit}",
                    "weather_code": self._get_weather_code(
                        current_data["weather"][0]["id"]
                    ),
                    "apparent_temperature": int(
                        round(current_data["main"]["feels_like"])
                    ),
                    "columns": columns,
                    "current_column": 0,
                    "sunrise_column": sunrise_column,
                    "sunset_column": sunset_column,
                    "place": {
                        "name": current_data["name"],
                        "area": current_data.get("sys", {}).get("state", ""),
                        "country": current_data["sys"]["country"],
                    },
                    "units": units,
                    "hide_location": self.config.get("hide_location", False),
                    "show_area_name": self.config.get("show_area_name", True),
                },
            }
        ]

    def _get_weather_code(self, weather_id: int) -> str:
        """Convert OpenWeatherMap weather ID to weather code."""
        if weather_id >= 200 and weather_id < 300:
            return "thunderstorm"
        elif weather_id >= 300 and weather_id < 400:
            return "drizzle"
        elif weather_id >= 500 and weather_id < 600:
            return "rain"
        elif weather_id >= 600 and weather_id < 700:
            return "snow"
        elif weather_id >= 700 and weather_id < 800:
            return "mist"
        elif weather_id == 800:
            return "clear"
        elif weather_id > 800 and weather_id < 900:
            return "partly_cloudy"
        else:
            return "unknown"

    def _get_weather_emoji(self, weather_code: str) -> str:
        """Get emoji for weather condition."""
        emoji_map = {
            "clear": "☀️",
            "partly_cloudy": "⛅",
            "cloudy": "☁️",
            "rain": "🌧️",
            "drizzle": "🌦️",
            "thunderstorm": "⛈️",
            "snow": "❄️",
            "mist": "🌫️",
            "unknown": "🌡️",
        }
        return emoji_map.get(weather_code, "🌡️")

    def get_weather_description(self, weather_code: str) -> str:
        """Get human-readable weather description from weather code."""
        descriptions = {
            "clear": "Clear",
            "partly_cloudy": "Partly Cloudy",
            "cloudy": "Cloudy",
            "rain": "Rain",
            "drizzle": "Drizzle",
            "thunderstorm": "Thunderstorm",
            "snow": "Snow",
            "mist": "Mist",
            "unknown": "Unknown",
        }
        return descriptions.get(weather_code, "Unknown")

    def render(self) -> None:
        """Render the weather module UI with Apple-inspired design."""
        data = self.fetch()
        if not data:
            ui.label("No weather data available").classes("text-gray-500")
            return

        weather = data[0]
        extra = weather.get("extra", {})
        columns = extra.get("columns", [])

        # Apple-inspired glassmorphism card
        with (
            ui.card().classes(
                "w-full backdrop-blur-xl bg-white/10 dark:bg-black/20 border border-white/20 dark:border-white/10 rounded-3xl p-6 shadow-xl"
            ),
            ui.column().classes("w-full gap-6"),
        ):
            # Header with current conditions
            with ui.row().classes("w-full justify-between items-center"):
                with ui.column().classes("gap-1"):
                    # Location and time
                    if not extra.get("hide_location", False):
                        place = extra.get("place", {})
                        location_parts = [place.get("name", "")]
                        if extra.get("show_area_name", True) and place.get("area"):
                            location_parts.append(place["area"])

                        location_text = ", ".join(filter(None, location_parts))
                        ui.label(location_text).classes(
                            DashboardStyles.BODY_TEXT
                            + " "
                            + DashboardStyles.FONT_MEDIUM
                            + " text-gray-600 dark:text-gray-300"
                        )

                    # Weather condition
                    ui.label(
                        self.get_weather_description(
                            extra.get("weather_code", "unknown")
                        )
                    ).classes(
                        DashboardStyles.TITLE_H3
                        + " "
                        + DashboardStyles.FONT_SEMIBOLD
                        + " text-gray-900 dark:text-white"
                    )

                # Temperature display
                temp_unit = "°C" if extra.get("units", "metric") == "metric" else "°F"
                with ui.column().classes("items-end gap-0.5"):
                    ui.label(f"{extra.get('temperature', '0')}").classes(
                        DashboardStyles.TITLE_H1
                        + " font-light text-gray-900 dark:text-white"
                    )
                    ui.label(
                        f"Feels like {extra.get('apparent_temperature', 0)}{temp_unit}"
                    ).classes(DashboardStyles.SUBTLE_TEXT + " dark:text-gray-400")

            # Weather details grid
            with ui.row().classes("w-full gap-4"):
                # Humidity
                if extra.get("humidity"):
                    with ui.card().classes(
                        f"flex-1 backdrop-blur-sm bg-white/5 dark:bg-black/10 border border-white/10 dark:border-white/5 rounded-2xl {DashboardStyles.PADDING_SM}"
                    ):
                        ui.label("Humidity").classes(
                            DashboardStyles.TEXT_XS
                            + " text-gray-500 dark:text-gray-400 mb-1"
                        )
                        ui.label(extra["humidity"]).classes(
                            DashboardStyles.BODY_TEXT
                            + " "
                            + DashboardStyles.FONT_MEDIUM
                            + " text-gray-900 dark:text-white"
                        )

                # Wind
                if extra.get("wind_speed"):
                    with ui.card().classes(
                        "flex-1 backdrop-blur-sm bg-white/5 dark:bg-black/10 border border-white/10 dark:border-white/5 rounded-2xl p-3"
                    ):
                        ui.label("Wind").classes(
                            "text-xs text-gray-500 dark:text-gray-400 mb-1"
                        )
                        ui.label(extra["wind_speed"]).classes(
                            "text-sm font-medium text-gray-900 dark:text-white"
                        )

                # Condition indicator
                with ui.card().classes(
                    "flex-1 backdrop-blur-sm bg-white/5 dark:bg-black/10 border border-white/10 dark:border-white/5 rounded-2xl p-3"
                ):
                    ui.label("Condition").classes(
                        "text-xs text-gray-500 dark:text-gray-400 mb-1"
                    )
                    weather_emoji = self._get_weather_emoji(
                        extra.get("weather_code", "unknown")
                    )
                    ui.label(weather_emoji).classes("text-lg")

            # Hourly forecast
            if columns:
                ui.label("Hourly Forecast").classes(
                    DashboardStyles.BODY_TEXT
                    + " "
                    + DashboardStyles.FONT_MEDIUM
                    + " text-gray-700 dark:text-gray-300 mb-3"
                )

                with ui.row().classes("w-full justify-between items-end gap-2 px-2"):
                    for i, column in enumerate(columns):
                        with ui.column().classes(
                            "flex flex-col items-center justify-end gap-2 flex-1"
                        ):
                            # Time label
                            show_time = i % 3 == 0 or i == extra.get(
                                "current_column", 0
                            )
                            if show_time:
                                ui.label(column["time"]).classes(
                                    DashboardStyles.TEXT_XS
                                    + " text-gray-500 dark:text-gray-400"
                                )

                            # Temperature bar container
                            with ui.element("div").classes(
                                "relative w-full h-16 flex items-end justify-center"
                            ):
                                # Precipitation indicator
                                if column.get("has_precipitation"):
                                    with ui.element("div").classes(
                                        "absolute top-0 left-1/2 transform -translate-x-1/2 "
                                        "text-blue-400 text-xs opacity-60"
                                    ):
                                        ui.label("💧")

                                # Temperature bar
                                bar_height = max(8, column["scale"] * 40)
                                is_current = i == extra.get("current_column", 0)

                                bar_classes = (
                                    "w-full rounded-t-lg transition-all duration-300 ease-out "
                                    "hover:scale-105 hover:shadow-lg"
                                )

                                if is_current:
                                    bar_classes += " bg-gradient-to-t from-blue-500 to-blue-400 shadow-lg"
                                else:
                                    bar_classes += (
                                        " bg-gradient-to-t from-blue-300 to-blue-200"
                                    )

                                ui.element("div").classes(bar_classes).style(
                                    f"height: {bar_height}px"
                                )

                            # Temperature value
                            temp_color = "text-gray-700 dark:text-gray-300"
                            if is_current:
                                temp_color = "text-blue-600 dark:text-blue-400"

                            temp_sign = "-" if column["temperature"] < 0 else ""
                            ui.label(
                                f"{temp_sign}{abs(column['temperature'])}°"
                            ).classes(
                                DashboardStyles.TEXT_XS
                                + " "
                                + DashboardStyles.FONT_MEDIUM
                                + f" {temp_color}"
                            )

            # Daylight indicator
            sunrise_col = extra.get("sunrise_column", 0)
            sunset_col = extra.get("sunset_column", 0)
            if columns and sunrise_col < len(columns) and sunset_col < len(columns):
                with ui.row().classes("w-full gap-2 mt-2"):
                    ui.label("🌅").classes("text-sm")
                    with ui.element("div").classes(
                        "flex-1 h-2 bg-gradient-to-r from-yellow-200/30 via-orange-200/50 to-yellow-200/30 rounded-full relative"
                    ):
                        # Sunrise marker
                        with ui.element("div").classes(
                            "absolute top-1/2 transform -translate-y-1/2 w-3 h-3 bg-yellow-400 rounded-full shadow-lg"
                        ):
                            pass
                        # Sunset marker
                        with ui.element("div").classes(
                            "absolute top-1/2 transform -translate-y-1/2 right-0 w-3 h-3 bg-orange-400 rounded-full shadow-lg"
                        ):
                            pass
                    ui.label("🌇").classes("text-sm")

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

        with ui.column().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.GAP_LG} {DashboardStyles.CONTAINER_CENTER} {DashboardStyles.PADDING_XL}"
        ):
            ui.label("Weather Forecast").classes(
                DashboardStyles.TITLE_H1 + " " + DashboardStyles.TEXT_CENTER + " mb-6"
            )

            # Main weather card
            with (
                ui.card().classes("w-full p-6 mb-6"),
                ui.column().classes("w-full gap-4 items-center"),
            ):
                # Location
                ui.label(weather["title"]).classes(
                    DashboardStyles.TITLE_H2 + " " + DashboardStyles.FONT_SEMIBOLD
                )

                # Current weather
                with ui.row().classes("w-full justify-center items-center gap-4"):
                    ui.label(extra.get("temperature", "")).classes(
                        DashboardStyles.TITLE_H1
                        + " "
                        + DashboardStyles.FONT_BOLD
                        + " text-blue-600"
                    )
                    with ui.column().classes("gap-2"):
                        ui.label(
                            self.get_weather_description(
                                extra.get("weather_code", "unknown")
                            )
                        ).classes(DashboardStyles.TITLE_H2 + " text-gray-600")
                        ui.label(
                            f"Feels like {extra.get('apparent_temperature', 0)}°{extra.get('units', 'metric') == 'metric' and 'C' or 'F'}"
                        ).classes(DashboardStyles.SUBTLE_TEXT)

                # Additional details
                with ui.row().classes("w-full justify-center gap-6 text-sm mt-4"):
                    if extra.get("humidity"):
                        ui.label(f"Humidity: {extra['humidity']}").classes(
                            DashboardStyles.BODY_TEXT
                            + " bg-gray-100 px-3 py-1 rounded-full"
                        )
                    if extra.get("wind_speed"):
                        ui.label(f"Wind: {extra['wind_speed']}").classes(
                            DashboardStyles.BODY_TEXT
                            + " bg-gray-100 px-3 py-1 rounded-full"
                        )

            # Hourly forecast section
            with ui.card().classes("w-full p-6"):
                ui.label("Hourly Forecast").classes(DashboardStyles.TITLE_H2 + " mb-4")
                self.render()

            # Configuration info
            if not self.config.get("api_key"):
                ui.label(
                    "💡 Configure OpenWeatherMap API key for real weather data"
                ).classes(
                    DashboardStyles.SUBTLE_TEXT
                    + " "
                    + DashboardStyles.TEXT_CENTER
                    + " mt-4"
                )
