"""ArXiv module implementation."""

from typing import Any

from nicegui import ui

from ...ui.styles import DashboardStyles
from ..extended import ExtendedModule


class ArxivModule(ExtendedModule):
    @property
    def id(self) -> str:
        return "arxiv"

    @property
    def name(self) -> str:
        return "Arxiv Papers"

    @property
    def icon(self) -> str:
        return "📚"

    @property
    def description(self) -> str:
        return "Latest academic papers and publications based on your interests"

    @property
    def version(self) -> str:
        return "1.0.0"

    def fetch(self) -> list[dict[str, Any]]:
        # Placeholder implementation
        return [
            {
                "title": "Quantum Computing Advances",
                "summary": "Recent breakthroughs in quantum computing algorithms and hardware implementations.",
                "link": "https://arxiv.org/example1",
                "published": "2025-07-30T10:00:00Z",
                "tags": ["quantum", "computing"],
                "extra": {"authors": ["Alice Johnson", "Bob Smith"]},
            },
            {
                "title": "Machine Learning in Bioinformatics",
                "summary": "Applications of deep learning techniques to protein structure prediction.",
                "link": "https://arxiv.org/example2",
                "published": "2025-07-29T14:30:00Z",
                "tags": ["machine learning", "bioinformatics"],
                "extra": {"authors": ["Carol Davis", "David Wilson"]},
            },
            {
                "title": "Renewable Energy Storage Solutions",
                "summary": "Novel battery technologies for efficient renewable energy storage.",
                "link": "https://arxiv.org/example3",
                "published": "2025-07-28T09:15:00Z",
                "tags": ["energy", "storage"],
                "extra": {"authors": ["Eve Brown", "Frank Miller"]},
            },
        ]

    def render(self) -> None:
        papers = self.fetch()
        # Show only the first paper in the main view
        if papers:
            paper = papers[0]
            with ui.element().classes("w-full"):
                # Title with link
                with ui.link(target=paper["link"]).classes("no-underline text-inherit"):
                    ui.label(paper["title"]).classes(
                        "text-lg font-bold hover-underline"
                    )

                # Summary
                ui.label(paper["summary"][:100] + "...").classes(
                    DashboardStyles.TEXT_MUTED + " mt-1"
                )

                # Footer with date and tags
                with ui.row().classes("items-center mt-2"):
                    ui.label(paper["published"][:10]).classes(
                        DashboardStyles.SUBTLE_TEXT
                    )
                    for tag in paper["tags"][:2]:  # Show only first 2 tags
                        ui.chip(tag).classes("mr-1")

    def render_detail(self) -> None:
        papers = self.fetch()
        ui.label(f"Latest {len(papers)} Papers").classes(
            DashboardStyles.TITLE_H1 + " mb-4"
        )

        for paper in papers:
            with ui.card().classes("w-full mb-4 card-hover"):
                # Title with link
                with ui.link(target=paper["link"]).classes("no-underline text-inherit"):
                    ui.label(paper["title"]).classes(
                        DashboardStyles.TITLE_H2 + " hover-underline"
                    )

                # Authors
                if "authors" in paper["extra"]:
                    ui.label(", ".join(paper["extra"]["authors"])).classes(
                        DashboardStyles.TEXT_MUTED + " italic"
                    )

                # Publication date
                ui.label(f"Published: {paper['published'][:10]}").classes(
                    DashboardStyles.SUBTLE_TEXT + " mt-1"
                )

                # Summary
                ui.label(paper["summary"]).classes(DashboardStyles.BODY_TEXT + " mt-2")

                # Tags
                with ui.row().classes("mt-2"):
                    for tag in paper["tags"]:
                        ui.chip(tag).classes("mr-1")

                # Action button
                with ui.row().classes("w-full justify-end mt-2"):
                    ui.button(
                        "View on ArXiv",
                        on_click=lambda link=paper["link"]: ui.run_javascript(
                            f'window.open("{link}", "_blank")'
                        ),
                    ).props("outline")
