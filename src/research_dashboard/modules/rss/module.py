"""RSS module implementation."""

from typing import Any

from nicegui import ui

from ..base import Module


class RssModule(Module):
    @property
    def id(self) -> str:
        return "rss"

    @property
    def name(self) -> str:
        return "RSS Feeds"

    @property
    def icon(self) -> str:
        return "📡"

    @property
    def description(self) -> str:
        return "Latest items from your RSS feeds"

    def fetch(self) -> list[dict[str, Any]]:
        # Placeholder implementation
        return [
            {
                "title": "Python 3.13 Release Candidate",
                "summary": "The Python development team has announced the first release candidate for Python 3.13.",
                "link": "https://example.com/python-313-rc1",
                "published": "2025-07-30T12:00:00Z",
                "tags": ["python", "release"],
                "extra": {"source": "Python Insider"},
            },
            {
                "title": "Advances in AI Research",
                "summary": "New paper explores the potential of transformer models in scientific discovery.",
                "link": "https://example.com/ai-research-advances",
                "published": "2025-07-29T08:30:00Z",
                "tags": ["ai", "research"],
                "extra": {"source": "AI Weekly"},
            },
            {
                "title": "Open Source Security Best Practices",
                "summary": "A comprehensive guide to securing your open source projects.",
                "link": "https://example.com/oss-security-guide",
                "published": "2025-07-28T14:20:00Z",
                "tags": ["security", "open-source"],
                "extra": {"source": "Open Source Security"},
            },
        ]

    def render(self) -> None:
        feeds = self.fetch()
        # Show only the first feed item in the main view
        if feeds:
            feed = feeds[0]
            with ui.element().classes("w-full"):
                # Title with link
                with ui.link(target=feed["link"]).classes("no-underline text-inherit"):
                    ui.label(feed["title"]).classes("text-lg font-bold hover-underline")

                # Summary
                ui.label(feed["summary"][:100] + "...").classes(
                    "text-gray-600 dark:text-gray-300 mt-1"
                )

                # Footer with date and tags
                with ui.row().classes("items-center mt-2"):
                    ui.label(feed["published"][:10]).classes("text-sm text-gray-500")
                    for tag in feed["tags"][:2]:  # Show only first 2 tags
                        ui.chip(tag).classes("mr-1")

    def render_detail(self) -> None:
        feeds = self.fetch()
        ui.label(f"Latest {len(feeds)} Feed Items").classes("text-2xl font-bold mb-4")

        for feed in feeds:
            with ui.card().classes("w-full mb-4 card-hover"):
                # Title with link
                with ui.link(target=feed["link"]).classes("no-underline text-inherit"):
                    ui.label(feed["title"]).classes("text-xl font-bold hover-underline")

                # Source
                if "source" in feed["extra"]:
                    ui.label(f"Source: {feed['extra']['source']}").classes(
                        "text-gray-600 dark:text-gray-300 italic"
                    )

                # Publication date
                ui.label(f"Published: {feed['published'][:10]}").classes(
                    "text-sm text-gray-500 mt-1"
                )

                # Summary
                ui.label(feed["summary"]).classes("mt-2")

                # Tags
                with ui.row().classes("mt-2"):
                    for tag in feed["tags"]:
                        ui.chip(tag).classes("mr-1")

                # Action button
                with ui.row().classes("w-full justify-end mt-2"):
                    ui.button(
                        "View Full Article",
                        on_click=lambda link=feed["link"]: ui.run_javascript(
                            f'window.open("{link}", "_blank")'
                        ),
                    ).props("outline")
