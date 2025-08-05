"""Animals module implementation."""

import random
from typing import Any
from urllib.parse import urljoin

import httpx
from nicegui import ui

from ...ui.styles import DashboardStyles
from ..extended import ExtendedModule


class AnimalsModule(ExtendedModule):
    @property
    def id(self) -> str:
        return "animals"

    @property
    def name(self) -> str:
        return "Animals"

    @property
    def icon(self) -> str:
        return "🐾"

    @property
    def description(self) -> str:
        return "Display random animal images from various sources"

    @property
    def category(self) -> str:
        return "entertainment"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def supported_features(self) -> list[str]:
        return ["image_display", "auto_refresh", "configurable"]

    def get_default_config(self) -> dict[str, Any]:
        return {
            "animal_type": "cat",
            "height": 200,
            "auto_refresh": False,
            "refresh_interval": 30,
            "show_title": True,
            "border_radius": 8,
        }

    def get_config_schema(self) -> dict[str, Any]:
        return {
            "animal_type": {
                "type": "select",
                "label": "Animal Type",
                "default": "cat",
                "description": "Choose the type of animal image to display",
                "options": [
                    {"label": "Cat", "value": "cat"},
                    {"label": "Dog", "value": "dog"},
                    {"label": "Duck", "value": "duck"},
                    {"label": "Fox", "value": "fox"},
                    {"label": "Rabbit", "value": "rabbit"},
                    {"label": "Capybara", "value": "capybara"},
                    {"label": "Hamster", "value": "hamster"},
                    {"label": "Random", "value": "random"},
                ],
            },
            "height": {
                "type": "number",
                "label": "Image Height",
                "default": 200,
                "description": "Height of the displayed image in pixels",
            },
            "auto_refresh": {
                "type": "boolean",
                "label": "Auto Refresh",
                "default": False,
                "description": "Automatically refresh the image at intervals",
            },
            "refresh_interval": {
                "type": "number",
                "label": "Refresh Interval (seconds)",
                "default": 30,
                "description": "How often to refresh the image when auto-refresh is enabled",
            },
            "show_title": {
                "type": "boolean",
                "label": "Show Title",
                "default": True,
                "description": "Show the animal type title above the image",
            },
            "border_radius": {
                "type": "number",
                "label": "Border Radius",
                "default": 8,
                "description": "Border radius for the image corners",
            },
        }

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.config = {**self.get_default_config(), **(config or {})}
        self.current_image_url = None
        self.current_animal_type = None
        self._timer = None

    def get_animal_apis(self) -> dict[str, str]:
        """Get API endpoints for different animal types."""
        return {
            "cat": "https://cataas.com/cat?json=true",
            "dog": "https://dog.ceo/api/breeds/image/random",
            "duck": "https://random-d.uk/api/v2/random",
            "fox": "https://randomfox.ca/floof/",
            "rabbit": "https://animals.maxz.dev/api/rabbit/random",
            "capybara": "https://animals.maxz.dev/api/capybara/random",
            "hamster": "https://animals.maxz.dev/api/hamster/random",
        }

    async def fetch_animal_image(self, animal_type: str) -> dict[str, Any]:
        """Fetch a random animal image from the specified API."""
        apis = self.get_animal_apis()

        if animal_type == "random":
            animal_type = random.choice(list(apis.keys()))

        api_url = apis.get(animal_type)
        if not api_url:
            raise ValueError(f"Unsupported animal type: {animal_type}")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(api_url)
                response.raise_for_status()
                data = response.json()

                # Extract image URL from response
                image_url = self._extract_image_url(data, animal_type, api_url)

                return {
                    "title": f"Random {animal_type.title()}",
                    "image_url": image_url,
                    "animal_type": animal_type,
                    "api_url": api_url,
                }
        except Exception as e:
            raise Exception(f"Failed to fetch {animal_type} image: {str(e)}") from e

    def _extract_image_url(self, data: dict, animal_type: str, api_url: str) -> str:
        """Extract image URL from API response."""
        if animal_type == "cat":
            # Cat API returns {url: "https://cataas.com/cat/..."}
            base_url = "https://cataas.com"
            return urljoin(base_url, data["url"])
        elif animal_type == "dog":
            # Dog API returns {message: "https://images.dog.ceo/..."}
            return data["message"]
        elif animal_type == "duck":
            # Duck API returns {url: "https://random-d.uk/api/v2/..."}
            return data["url"]
        elif animal_type == "fox":
            # Fox API returns {image: "https://randomfox.ca/..."}
            return data["image"]
        elif animal_type in ["rabbit", "capybara", "hamster"]:
            # Maxz.dev APIs return {url: "https://cdn.maxz.dev/..."}
            return data["url"]
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch animal image data."""
        try:
            animal_type = self.config.get("animal_type", "cat")

            # For synchronous fetch, use httpx sync client
            apis = self.get_animal_apis()

            if animal_type == "random":
                animal_type = random.choice(list(apis.keys()))

            api_url = apis.get(animal_type)
            if not api_url:
                return []

            with httpx.Client(timeout=10.0) as client:
                response = client.get(api_url)
                response.raise_for_status()
                data = response.json()

                image_url = self._extract_image_url(data, animal_type, api_url)

                self.current_image_url = image_url
                self.current_animal_type = animal_type

                return [
                    {
                        "title": f"Random {animal_type.title()}",
                        "image_url": image_url,
                        "animal_type": animal_type,
                        "api_url": api_url,
                    }
                ]
        except Exception as e:
            self._handle_error(e)
            return []

    def render(self) -> None:
        """Render the animal image module."""
        data = self.fetch()

        if not data:
            with ui.element().classes("w-full text-center p-4"):
                ui.label("Failed to load image").classes("text-red-500")
                ui.button("Retry", on_click=self._refresh_image).classes("mt-2")
            return

        item = data[0]
        height = self.config.get("height", 200)
        show_title = self.config.get("show_title", True)
        border_radius = self.config.get("border_radius", 8)

        with ui.element().classes(f"{DashboardStyles.FULL_WIDTH} text-center"):
            if show_title:
                ui.label(item["title"]).classes(DashboardStyles.TITLE_H2 + " mb-2")

            # Image with error handling using JavaScript
            with ui.element().classes("w-full"):
                image = (
                    ui.image(item["image_url"])
                    .classes(
                        f"{DashboardStyles.FULL_WIDTH} object-cover rounded-lg border-2 border-gray-200 dark:border-gray-700"
                    )
                    .style(f"height: {height}px; border-radius: {border_radius}px;")
                )
                # Add error handling using JavaScript
                image.on(
                    "error",
                    lambda e: ui.run_javascript(
                        f'this.src="https://via.placeholder.com/{height}x{height}?text=Image+Not+Available"'
                    ),
                )

            # Refresh button
            ui.button(
                "New Image", icon="refresh", on_click=self._refresh_image
            ).classes("mt-2 bg-blue-500 text-white")

    def render_detail(self) -> None:
        """Render detailed view with more options."""
        ui.label("Animals Gallery").classes(DashboardStyles.TITLE_H1 + " mb-4")

        # Configuration controls
        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} mb-4 {DashboardStyles.PADDING_LG}"
        ):
            ui.label("Settings").classes("text-lg font-semibold mb-2")
            self.render_config_ui()

        # Main image display
        self.render()

        # Additional information
        if self.current_image_url and self.current_animal_type:
            with ui.card().classes(
                f"{DashboardStyles.FULL_WIDTH} mt-4 {DashboardStyles.PADDING_LG}"
            ):
                ui.label("Current Image Info").classes(
                    DashboardStyles.TITLE_H2 + " mb-2"
                )
                ui.label(f"Animal Type: {self.current_animal_type.title()}").classes(
                    DashboardStyles.TEXT_SM
                )
                ui.label(f"Image URL: {self.current_image_url}").classes(
                    DashboardStyles.TEXT_SM
                    + " "
                    + DashboardStyles.TEXT_SECONDARY
                    + " break-all"
                )

                # Copy URL button
                ui.button(
                    "Copy Image URL",
                    icon="content_copy",
                    on_click=lambda: ui.run_javascript(
                        f"navigator.clipboard.writeText('{self.current_image_url}')"
                    ),
                ).classes("mt-2")

    def _refresh_image(self) -> None:
        """Refresh the current image."""
        try:
            self.fetch()
            ui.notify("Image refreshed!", type="positive")
        except Exception as e:
            self._handle_error(e)
            ui.notify(f"Failed to refresh: {str(e)}", type="negative")

    def _initialize_module(self) -> None:
        """Initialize module-specific resources."""
        # Set up auto-refresh if enabled
        if self.config.get("auto_refresh", False):
            self._setup_auto_refresh()

    def _setup_auto_refresh(self) -> None:
        """Set up automatic image refresh."""
        self.config.get("refresh_interval", 30)

        # This would be implemented with NiceGUI's timer functionality
        # For now, it's a placeholder
        pass

    def _shutdown_module(self) -> None:
        """Clean up module-specific resources."""
        # Clean up any timers or resources
        pass

    def has_cache(self) -> bool:
        """Check if module uses caching."""
        return True

    def has_persistence(self) -> bool:
        """Check if module requires persistent storage."""
        return False
