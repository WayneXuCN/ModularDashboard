"""RSS module implementation."""

import re
import time
from datetime import datetime
from typing import Any

import feedparser
from loguru import logger
from nicegui import ui

from ..extended import ExtendedModule


class RssModule(ExtendedModule):
    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        # Initialize configuration attributes
        self.feed_urls = self.config.get("feed_urls", ["https://waynexucn.github.io/feed.xml"])
        self.refresh_interval = self.config.get("refresh_interval", 3600)
        self.fetch_limit = self.config.get("fetch_limit", 5)
        self.show_author = self.config.get("show_author", True)
        self.show_description = self.config.get("show_description", True)
        self.show_date = self.config.get("show_date", True)
        self.show_image = self.config.get("show_image", True)
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

    @property
    def version(self) -> str:
        return "1.0.0"

    def fetch(self) -> list[dict[str, Any]]:

        # Use cache management
        cache = self.get_cache(self.refresh_interval)
        cached_data = cache.get("feeds")
        if cached_data:
            return cached_data

        all_entries = []
        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                items = feed.entries[: self.fetch_limit]
                for entry in items:
                    title = getattr(entry, "title", "No title")
                    link = getattr(entry, "link", "#")
                    description = getattr(entry, "description", "No description")
                    clean_desc = re.sub("<[^<]+?>", "", description)[:200] + "..."
                    pub_date = getattr(
                        entry, "published", datetime.now().strftime("%Y-%m-%d")
                    )
                    updated_date = getattr(entry, "updated", pub_date)
                    author = getattr(entry, "author", "Unknown")
                    source = url.split("/")[2] if len(url.split("/")) > 2 else url

                    # 提取图片链接
                    image_url = None
                    if hasattr(entry, "media_content") and entry.media_content:
                        image_url = entry.media_content[0].get("url")
                    elif hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                        image_url = entry.media_thumbnail[0].get("url")
                    elif hasattr(entry, "image"):
                        image_url = getattr(entry, "image", None)

                    fields = [
                        ("title", title),
                        ("link", link),
                        ("updated", updated_date),
                        ("tags", []),
                        ("extra", {"source": source}),
                    ]

                    if self.show_author:
                        fields.append(("author", author))
                    if self.show_description:
                        fields.append(("summary", clean_desc))
                    if self.show_date:
                        fields.append(("published", pub_date))
                    if self.show_image and image_url:
                        fields.append(("image", image_url))

                    all_entries.append(dict(fields))

            except Exception as e:
                print(f"Error fetching RSS feed {url}: {e}")
        all_entries.sort(key=lambda x: x.get("published", ""), reverse=True)

        # Cache the results
        cache.set("feeds", all_entries)
        return all_entries

    def render(self) -> None:
        cache = self.get_cache(self.refresh_interval)
        feeds = cache.get("feeds")
        if feeds is None:
            feeds = self.fetch()
        show_limit = getattr(self, "show_limit", 5)
        items = feeds[:show_limit] if feeds else []
        with ui.column().classes("w-full gap-2"):
            for feed in items:
                with ui.row().classes("items-center gap-4"):
                    with ui.link(target=feed["link"]).classes(
                        "font-bold text-primary text-base hover-underline"
                    ):
                        ui.label(feed["title"])
                    if "published" in feed:
                        ui.label(feed["published"][:10]).classes(
                            "text-xs text-gray-500"
                        )
                    if "author" in feed:
                        ui.label(feed["author"]).classes("text-xs text-gray-600")
                    if "source" in feed["extra"]:
                        ui.label(feed["extra"]["source"]).classes(
                            "text-xs text-gray-400"
                        )

    def render_detail(self) -> None:
        cache = self.get_cache(self.refresh_interval)
        feeds = cache.get("feeds")
        if feeds is None:
            feeds = self.fetch()

        with ui.row().classes("w-full justify-between items-center mb-4"):
            ui.label(f"Latest {self.fetch_limit} Feed Posts").classes(
                "text-2xl font-bold"
            )
            ui.button(icon="refresh", on_click=self._refresh_feeds).props(
                "round flat"
            ).classes("text-sm")

        with ui.grid().classes("grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"):
            for feed in feeds:
                with (
                    ui.link(target=feed["link"]).classes("no-underline"),
                    ui.card().classes(
                        "mb-4 card-hover hover:shadow-lg transition-shadow duration-200 cursor-pointer"
                    ),
                ):
                    if self.show_image and "image" in feed:
                        ui.image(feed["image"]).classes(
                            "w-full h-40 object-cover mb-2 rounded"
                        )
                    ui.label(feed["title"]).classes(
                        "text-xl font-bold text-center mb-2 hover-underline"
                    )
                    with ui.row().classes("justify-between items-center mb-1"):
                        if "author" in feed:
                            ui.label(f"{feed['author']}").classes(
                                "text-gray-500 text-sm"
                            )
                        if "source" in feed["extra"]:
                            ui.label(f"{feed['extra']['source']}").classes(
                                "text-gray-600 dark:text-gray-300 italic text-sm"
                            )
                        if "published" in feed:
                            ui.label(f"{feed['published'][:10]}").classes(
                                "text-sm text-gray-500"
                            )
                    if "summary" in feed:
                        ui.label(feed["summary"]).classes(
                            "mt-2 text-gray-700 line-clamp-3"
                        )

    def _refresh_feeds(self):
        """refetch feeds and update the UI"""
        self.clear_cache()
        ui.navigate.reload()
        ui.notify("Refreshed", type="positive")

    def clear_cache(self):
        """Clear RSS cache"""
        cache = self.get_cache(self.refresh_interval)
        cache.delete("feeds")
        logger.info("Cleared RSS feeds cache")
    
    def has_cache(self) -> bool:
        """RSS module uses caching."""
        return True
