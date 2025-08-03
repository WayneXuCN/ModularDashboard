"""GitHub module implementation."""

from typing import Any

from nicegui import ui

from ..extended import ExtendedModule


class GithubModule(ExtendedModule):
    @property
    def id(self) -> str:
        return "github"

    @property
    def name(self) -> str:
        return "GitHub Activity"

    @property
    def icon(self) -> str:
        return "🐙"

    @property
    def description(self) -> str:
        return "Your recent GitHub activity"

    @property
    def version(self) -> str:
        return "1.0.0"

    def fetch(self) -> list[dict[str, Any]]:
        # Placeholder implementation
        return [
            {
                "title": "New commit in modular-dashboard",
                "summary": "Added support for native desktop app mode",
                "link": "https://github.com/WayneXuCN/ModularDashboard/commit/abc123",
                "published": "2025-07-30T15:30:00Z",
                "tags": ["commit", "modular-dashboard"],
                "extra": {"author": "dev-user"},
            },
            {
                "title": "Issue opened in nicegui",
                "summary": "Dark mode theme not applying correctly",
                "link": "https://github.com/zauberzeug/nicegui/issues/456",
                "published": "2025-07-30T10:15:00Z",
                "tags": ["issue", "nicegui"],
                "extra": {"author": "bug-reporter"},
            },
            {
                "title": "Pull request merged in arxiv-api",
                "summary": "Improved search performance for large datasets",
                "link": "https://github.com/example/arxiv-api/pull/789",
                "published": "2025-07-29T16:45:00Z",
                "tags": ["pull-request", "arxiv-api"],
                "extra": {"author": "contributor"},
            },
        ]

    def render(self) -> None:
        activities = self.fetch()
        # Show only the first activity in the main view
        if activities:
            activity = activities[0]
            with ui.element().classes("w-full"):
                # Title with link
                with ui.link(target=activity["link"]).classes(
                    "no-underline text-inherit"
                ):
                    ui.label(activity["title"]).classes(
                        "text-lg font-bold hover-underline"
                    )

                # Summary
                ui.label(activity["summary"][:100] + "...").classes(
                    "text-gray-600 dark:text-gray-300 mt-1"
                )

                # Footer with date and tags
                with ui.row().classes("items-center mt-2"):
                    ui.label(activity["published"][:10]).classes(
                        "text-sm text-gray-500"
                    )
                    for tag in activity["tags"][:2]:  # Show only first 2 tags
                        ui.chip(tag).classes("mr-1")

    def render_detail(self) -> None:
        activities = self.fetch()
        ui.label(f"Latest {len(activities)} Activities").classes(
            "text-2xl font-bold mb-4"
        )

        for activity in activities:
            with ui.card().classes("w-full mb-4 card-hover"):
                # Title with link
                with ui.link(target=activity["link"]).classes(
                    "no-underline text-inherit"
                ):
                    ui.label(activity["title"]).classes(
                        "text-xl font-bold hover-underline"
                    )

                # Author
                if "author" in activity["extra"]:
                    ui.label(f"Author: {activity['extra']['author']}").classes(
                        "text-gray-600 dark:text-gray-300 italic"
                    )

                # Publication date
                ui.label(f"Published: {activity['published'][:10]}").classes(
                    "text-sm text-gray-500 mt-1"
                )

                # Summary
                ui.label(activity["summary"]).classes("mt-2")

                # Tags
                with ui.row().classes("mt-2"):
                    for tag in activity["tags"]:
                        ui.chip(tag).classes("mr-1")

                # Action button
                with ui.row().classes("w-full justify-end mt-2"):
                    ui.button(
                        "View on GitHub",
                        on_click=lambda link=activity["link"]: ui.run_javascript(
                            f'window.open("{link}", "_blank")'
                        ),
                    ).props("outline")
