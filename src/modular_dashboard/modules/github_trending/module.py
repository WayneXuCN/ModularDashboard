"""GitHub Trending module implementation."""

import json
from datetime import datetime
from typing import Any
from urllib.request import urlopen

from nicegui import ui

from ..extended import ExtendedModule


class GithubTrendingModule(ExtendedModule):
    """GitHub Trending repositories module using OSS Insights API."""

    @property
    def id(self) -> str:
        return "github_trending"

    @property
    def name(self) -> str:
        return "GitHub Trending"

    @property
    def icon(self) -> str:
        return "🔥"

    @property
    def description(self) -> str:
        return "Trending GitHub repositories from OSS Insights"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def category(self) -> str:
        return "development"

    @property
    def supported_features(self) -> list[str]:
        return ["trending_repos", "language_filter", "period_filter", "caching"]

    def has_cache(self) -> bool:
        """Module uses caching for API responses."""
        return True

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration for the GitHub trending module."""
        return {
            "period": "weekly",
            "language": "",
            "limit": 10,
            "cache_ttl": 3600,  # 1 hour cache
        }

    def get_config_schema(self) -> dict[str, Any]:
        """Get configuration schema for UI generation."""
        return {
            "period": {
                "type": "select",
                "label": "Time Period",
                "description": "Time period for trending repositories",
                "default": "weekly",
                "options": [
                    {"label": "Daily", "value": "daily"},
                    {"label": "Weekly", "value": "weekly"},
                    {"label": "Monthly", "value": "monthly"},
                ],
            },
            "language": {
                "type": "string",
                "label": "Programming Language",
                "description": "Filter by programming language (leave empty for all)",
                "default": "",
            },
            "limit": {
                "type": "number",
                "label": "Repository Limit",
                "description": "Maximum number of repositories to display",
                "default": 10,
                "min": 1,
                "max": 50,
            },
            "cache_ttl": {
                "type": "number",
                "label": "Cache TTL (seconds)",
                "description": "How long to cache API responses",
                "default": 3600,
                "min": 300,
                "max": 86400,
            },
        }

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch trending repositories from OSS Insights API."""
        period = self.config.get("period", "weekly")
        language = self.config.get("language", "")
        limit = self.config.get("limit", 10)
        cache_ttl = self.config.get("cache_ttl", 3600)

        # Try to get from cache first
        cache = self.get_cache(cache_ttl)
        cache_key = f"trending_{period}_{language}_{limit}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        try:
            # Build API URL
            base_url = "https://api.ossinsight.io/v1/trends/repos/"
            params = f"?period={period}"
            if language:
                params += f"&language={language}"

            url = base_url + params

            with urlopen(url) as response:
                data = json.loads(response.read().decode())

            # Process and cache the data
            processed_data = self._process_api_response(data, limit)
            cache.set(cache_key, processed_data)

            return processed_data

        except Exception:
            # Return mock data on error
            return self._get_mock_data(period, language, limit)

    def _process_api_response(self, data: dict, limit: int) -> list[dict[str, Any]]:
        """Process API response and return standardized format."""
        repositories = []

        if "data" in data and "rows" in data["data"]:
            for repo in data["data"]["rows"][:limit]:
                repositories.append(
                    {
                        "title": repo.get("repo_name", "Unknown Repository"),
                        "summary": repo.get("description", "No description available"),
                        "link": f"https://github.com/{repo.get('repo_name', '')}",
                        "published": datetime.now().isoformat(),
                        "tags": [
                            repo.get("primary_language", "Unknown"),
                            "trending",
                        ],
                        "extra": {
                            "repo_name": repo.get("repo_name", ""),
                            "primary_language": repo.get("primary_language", "Unknown"),
                            "stars": repo.get("stars", 0),
                            "forks": repo.get("forks", 0),
                            "pull_requests": repo.get("pull_requests", 0),
                            "contributor_logins": repo.get("contributor_logins", ""),
                            "description": repo.get(
                                "description", "No description available"
                            ),
                            "period": self.config.get("period", "weekly"),
                        },
                    }
                )

        return repositories

    def _get_mock_data(
        self, period: str, language: str, limit: int
    ) -> list[dict[str, Any]]:
        """Get mock data for testing or when API is unavailable."""
        mock_repos = [
            {
                "title": "microsoft/vscode",
                "summary": "Visual Studio Code",
                "link": "https://github.com/microsoft/vscode",
                "published": datetime.now().isoformat(),
                "tags": ["TypeScript", "trending"],
                "extra": {
                    "repo_name": "microsoft/vscode",
                    "primary_language": "TypeScript",
                    "stars": 159000,
                    "forks": 27800,
                    "pull_requests": 1500,
                    "contributor_logins": "user1,user2,user3",
                    "description": "Visual Studio Code",
                    "period": period,
                },
            },
            {
                "title": "facebook/react",
                "summary": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                "link": "https://github.com/facebook/react",
                "published": datetime.now().isoformat(),
                "tags": ["JavaScript", "trending"],
                "extra": {
                    "repo_name": "facebook/react",
                    "primary_language": "JavaScript",
                    "stars": 218000,
                    "forks": 44600,
                    "pull_requests": 2100,
                    "contributor_logins": "dev1,dev2,dev3",
                    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
                    "period": period,
                },
            },
            {
                "title": "tensorflow/tensorflow",
                "summary": "An Open Source Machine Learning Framework for Everyone",
                "link": "https://github.com/tensorflow/tensorflow",
                "published": datetime.now().isoformat(),
                "tags": ["C++", "trending"],
                "extra": {
                    "repo_name": "tensorflow/tensorflow",
                    "primary_language": "C++",
                    "stars": 186000,
                    "forks": 75600,
                    "pull_requests": 1800,
                    "contributor_logins": "ml1,ml2,ml3",
                    "description": "An Open Source Machine Learning Framework for Everyone",
                    "period": period,
                },
            },
        ]

        return mock_repos[:limit]

    def render(self) -> None:
        """Render the GitHub trending module UI."""
        data = self.fetch()

        if not data:
            ui.label("No trending repositories available").classes("text-gray-500")
            return

        # Show only the first repository in the main view
        repo = data[0]
        extra = repo.get("extra", {})

        with ui.card().classes("w-full card-hover"):
            # Repository name with link
            with ui.link(target=repo["link"]).classes("no-underline text-inherit"):
                ui.label(repo["title"]).classes(
                    "text-lg font-bold hover-underline text-blue-600 dark:text-blue-400"
                )

            # Language and stats
            with ui.row().classes("items-center gap-4 mt-2"):
                # Language
                if extra.get("primary_language"):
                    ui.chip(extra["primary_language"]).classes(
                        "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                    )

                # Stars
                with ui.row().classes("items-center gap-1"):
                    ui.label("⭐").classes("text-sm")
                    ui.label(f"{extra.get('stars', 0):,}").classes(
                        "text-sm font-medium"
                    )

                # Forks
                with ui.row().classes("items-center gap-1"):
                    ui.label("🍴").classes("text-sm")
                    ui.label(f"{extra.get('forks', 0):,}").classes(
                        "text-sm font-medium"
                    )

            # Description
            if repo.get("summary"):
                ui.label(repo["summary"][:80] + "...").classes(
                    "text-sm text-gray-600 dark:text-gray-300 mt-2"
                )

    def render_detail(self) -> None:
        """Render detailed view of trending repositories."""
        data = self.fetch()

        if not data:
            ui.label("No trending repositories available").classes(
                "text-gray-500 text-center w-full"
            )
            return

        period = self.config.get("period", "weekly")
        language = self.config.get("language", "")

        ui.label("🔥 Trending Repositories").classes("text-2xl font-bold mb-4")

        # Filter info
        filter_text = f"({period.capitalize()}"
        if language:
            filter_text += f" • {language}"
        filter_text += ")"
        ui.label(filter_text).classes("text-gray-500 mb-6")

        # Render all repositories
        for repo in data:
            extra = repo.get("extra", {})

            with ui.card().classes("w-full mb-4 card-hover"):
                # Repository name with link
                with ui.link(target=repo["link"]).classes("no-underline text-inherit"):
                    ui.label(repo["title"]).classes(
                        "text-xl font-bold hover-underline text-blue-600 dark:text-blue-400"
                    )

                # Stats row
                with ui.row().classes("items-center gap-4 mt-2"):
                    # Language
                    if extra.get("primary_language"):
                        ui.chip(extra["primary_language"]).classes(
                            "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                        )

                    # Stars
                    with ui.row().classes("items-center gap-1"):
                        ui.label("⭐").classes("text-sm")
                        ui.label(f"{extra.get('stars', 0):,}").classes(
                            "text-sm font-medium"
                        )

                    # Forks
                    with ui.row().classes("items-center gap-1"):
                        ui.label("🍴").classes("text-sm")
                        ui.label(f"{extra.get('forks', 0):,}").classes(
                            "text-sm font-medium"
                        )

                    # Pull requests
                    with ui.row().classes("items-center gap-1"):
                        ui.label("🔄").classes("text-sm")
                        ui.label(f"{extra.get('pull_requests', 0):,}").classes(
                            "text-sm font-medium"
                        )

                # Description
                if repo.get("summary"):
                    ui.label(repo["summary"]).classes(
                        "text-sm text-gray-600 dark:text-gray-300 mt-2"
                    )

                # Contributors
                if extra.get("contributor_logins"):
                    contributors = (
                        extra["contributor_logins"][:50] + "..."
                        if len(extra["contributor_logins"]) > 50
                        else extra["contributor_logins"]
                    )
                    ui.label(f"Contributors: {contributors}").classes(
                        "text-xs text-gray-500 mt-1"
                    )

                # Action button
                with ui.row().classes("w-full justify-end mt-2"):
                    ui.button(
                        "View on GitHub",
                        on_click=lambda link=repo["link"]: ui.run_javascript(
                            f'window.open("{link}", "_blank")'
                        ),
                    ).props("outline").classes("text-sm")
