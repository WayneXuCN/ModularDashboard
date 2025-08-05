"""Random Fact module implementation."""

import json
from datetime import datetime
from typing import Any
from urllib.request import urlopen

from nicegui import ui

from ..extended import ExtendedModule


class RandomFactModule(ExtendedModule):
    """Random Fact module that fetches and processes random facts with AI translation."""

    @property
    def id(self) -> str:
        return "random_fact"

    @property
    def name(self) -> str:
        return "Random Fact"

    @property
    def icon(self) -> str:
        return "📝"

    @property
    def description(self) -> str:
        return "Random facts with AI translation and commentary"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def category(self) -> str:
        return "entertainment"

    @property
    def supported_features(self) -> list[str]:
        return ["ai_translation", "caching", "fact_processing"]

    def has_cache(self) -> bool:
        """Module uses caching for API responses."""
        return True

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration for the Random Fact module."""
        return {
            "api_key": "",  # SiliconFlow API key
            "model": "Qwen/Qwen3-8B",  # Default model
            "cache_ttl": 7200,  # 2 hours cache
            "max_facts": 5,  # Maximum number of facts to store
            "enable_ai": False,  # Enable AI processing
        }

    def get_config_schema(self) -> dict[str, Any]:
        """Get configuration schema for UI generation."""
        return {
            "api_key": {
                "type": "string",
                "label": "SiliconFlow API Key",
                "description": "API key for SiliconFlow AI service",
                "default": "",
            },
            "model": {
                "type": "string",
                "label": "AI Model",
                "description": "Model to use for processing facts",
                "default": "Qwen/Qwen3-8B",
            },
            "cache_ttl": {
                "type": "number",
                "label": "Cache TTL (seconds)",
                "description": "How long to cache facts",
                "default": 7200,
                "min": 300,
                "max": 86400,
            },
            "max_facts": {
                "type": "number",
                "label": "Maximum Facts",
                "description": "Maximum number of facts to store",
                "default": 5,
                "min": 1,
                "max": 20,
            },
            "enable_ai": {
                "type": "boolean",
                "label": "Enable AI Processing",
                "description": "Use AI to translate and enhance facts",
                "default": True,
            },
        }

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch random facts from API and process them."""
        cache_ttl = self.config.get("cache_ttl", 7200)
        max_facts = self.config.get("max_facts", 5)
        enable_ai = self.config.get("enable_ai", True)

        # Try to get from cache first
        cache = self.get_cache(cache_ttl)
        cached_data = cache.get("random_facts")

        if cached_data:
            return cached_data[:max_facts]

        try:
            # Fetch new fact
            fact_data = self._fetch_random_fact()

            if enable_ai and self.config.get("api_key"):
                # Process with AI
                processed_fact = self._process_with_ai(fact_data)
            else:
                # Use basic processing
                processed_fact = self._process_basic(fact_data)

            # Store in cache
            facts = [processed_fact]
            cache.set("random_facts", facts)

            return facts

        except Exception:
            # Return mock data on error
            return self._get_mock_data()

    def _fetch_random_fact(self) -> dict[str, Any]:
        """Fetch a random fact from the API."""
        api_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

        with urlopen(api_url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data

    def _process_with_ai(self, raw_fact: dict[str, Any]) -> dict[str, Any]:
        """Process fact with AI translation and commentary."""
        api_key = self.config.get("api_key")
        model = self.config.get("model", "Qwen/Qwen3-8B")

        if not api_key:
            return self._process_basic(raw_fact)

        url = "https://api.siliconflow.cn/v1/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": """
                    你是一个 random fact 理解助手。请将用户提供的英文句子翻译为中文，并在下一行用简洁语言对内容进行自然的补充说明。注意：不要使用任何标题、标签或"补充："等前缀，直接输出翻译和补充内容各占一行。
                    示例输入：
                    PEZ candy even comes in a Coffee flavor.

                    示例输出：
                    PEZ糖果甚至还有咖啡味的。
                    这种独特的咖啡味PEZ糖果是该品牌众多创意口味之一，旨在为消费者提供意想不到的趣味体验。
                    """,
                },
                {"role": "user", "content": raw_fact["text"]},
            ],
            "stream": False,
            "max_tokens": 512,
            "enable_thinking": False,
            "response_format": {"type": "text"},
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            from urllib.error import URLError
            from urllib.request import Request

            req = Request(
                url, json.dumps(payload).encode(), headers=headers, method="POST"
            )
            with urlopen(req, timeout=30) as response:
                ai_response = json.loads(response.read().decode())

                if "choices" not in ai_response or not ai_response["choices"]:
                    return self._process_basic(raw_fact)

                content = ai_response["choices"][0]["message"]["content"]
                return self._create_fact_dict(raw_fact, content, model)

        except (URLError, KeyError, json.JSONDecodeError):
            return self._process_basic(raw_fact)

    def _process_basic(self, raw_fact: dict[str, Any]) -> dict[str, Any]:
        """Process fact without AI - basic translation only."""
        # Simple English to Chinese mapping for common words
        fact_text = raw_fact.get("text", "")
        basic_translation = f"[英文原文: {fact_text}]"

        return self._create_fact_dict(raw_fact, basic_translation, "basic")

    def _create_fact_dict(
        self, raw_fact: dict[str, Any], content: str, source: str
    ) -> dict[str, Any]:
        """Create standardized fact dictionary."""
        return {
            "title": f"Random Fact #{raw_fact.get('id', 'unknown')}",
            "summary": content.split("\n")[0] if "\n" in content else content[:100],
            "link": f"https://uselessfacts.jsph.pl/api/v2/facts/random?id={raw_fact.get('id', '')}",
            "published": datetime.now().isoformat(),
            "tags": ["fact", "random"],
            "extra": {
                "fact_id": raw_fact.get("id", "unknown"),
                "fact_text": raw_fact.get("text", ""),
                "content": content,
                "source": source,
                "language": "zh" if source != "basic" else "en",
            },
        }

    def _get_mock_data(self) -> list[dict[str, Any]]:
        """Get mock data for testing or when API is unavailable."""
        mock_fact = {
            "title": "Random Fact #mock",
            "summary": "这是一个模拟的随机事实，用于演示目的。",
            "link": "https://uselessfacts.jsph.pl/api/v2/facts/random",
            "published": datetime.now().isoformat(),
            "tags": ["fact", "random", "mock"],
            "extra": {
                "fact_id": "mock",
                "fact_text": "This is a mock random fact for demonstration purposes.",
                "content": "这是一个模拟的随机事实，用于演示目的。当API不可用时显示此内容。",
                "source": "mock",
                "language": "zh",
            },
        }
        return [mock_fact]

    def render(self) -> None:
        """Render the Random Fact module UI."""
        data = self.fetch()

        if not data:
            ui.label("No facts available").classes("text-gray-500")
            return

        # Show only the first fact in the main view
        fact = data[0]
        extra = fact.get("extra", {})

        with ui.card().classes("w-full card-hover"):
            # Title
            ui.label("📝 Random Fact").classes("text-lg font-bold mb-2")

            # Original fact text
            if extra.get("fact_text"):
                ui.label(extra["fact_text"]).classes(
                    "text-sm text-gray-600 dark:text-gray-300 italic mb-2"
                )

            # Processed content
            if extra.get("content"):
                content_lines = extra["content"].split("\n")
                with ui.column().classes("w-full gap-1"):
                    for line in content_lines:
                        if line.strip():
                            ui.label(line.strip()).classes(
                                "text-sm text-gray-800 dark:text-gray-200"
                            )

            # Meta info
            with ui.row().classes("items-center gap-2 mt-2"):
                if extra.get("source"):
                    ui.label(f"Source: {extra['source']}").classes(
                        "text-xs text-gray-500"
                    )
                if extra.get("fact_id"):
                    ui.label(f"ID: {extra['fact_id']}").classes("text-xs text-gray-500")

    def render_detail(self) -> None:
        """Render detailed view of random facts."""
        data = self.fetch()

        if not data:
            ui.label("No facts available").classes("text-gray-500 text-center w-full")
            return

        ui.label("📝 Random Facts").classes("text-2xl font-bold mb-4")

        # Show all facts
        for fact in data:
            extra = fact.get("extra", {})

            with ui.card().classes("w-full mb-4 card-hover"):
                # Title
                ui.label(fact["title"]).classes("text-xl font-bold mb-2")

                # Original fact text
                if extra.get("fact_text"):
                    ui.label(extra["fact_text"]).classes(
                        "text-sm text-gray-600 dark:text-gray-300 italic mb-2"
                    )

                # Processed content
                if extra.get("content"):
                    content_lines = extra["content"].split("\n")
                    with ui.column().classes("w-full gap-1 mb-2"):
                        for line in content_lines:
                            if line.strip():
                                ui.label(line.strip()).classes(
                                    "text-sm text-gray-800 dark:text-gray-200"
                                )

                # Meta info and actions
                with ui.row().classes("items-center justify-between w-full mt-2"):
                    with ui.row().classes("items-center gap-2"):
                        if extra.get("source"):
                            ui.chip(extra["source"]).classes(
                                "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                            )
                        if extra.get("language"):
                            ui.chip(extra["language"].upper()).classes(
                                "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                            )

                    # Action buttons
                    with ui.row().classes("gap-2"):
                        ui.button(
                            "New Fact", icon="refresh", on_click=self._refresh_fact
                        ).props("outline").classes("text-sm")

                        if fact.get("link"):
                            ui.button(
                                "View Source",
                                icon="open_in_new",
                                on_click=lambda link=fact["link"]: ui.run_javascript(
                                    f'window.open("{link}", "_blank")'
                                ),
                            ).props("outline").classes("text-sm")

    def _refresh_fact(self) -> None:
        """Refresh fact data."""
        try:
            # Clear cache and fetch new data
            cache = self.get_cache()
            cache.delete("random_facts")

            # Re-render the detail view
            ui.notify("Fact refreshed successfully", type="positive")
            # Note: In a real implementation, you'd need to trigger a re-render
            # This is a simplified version
        except Exception as e:
            ui.notify(f"Failed to refresh fact: {str(e)}", type="negative")
