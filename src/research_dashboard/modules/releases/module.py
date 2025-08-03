"""Releases module for monitoring latest releases from multiple platforms."""

import json
import re
from datetime import datetime
from typing import Any
from urllib.request import urlopen

from nicegui import ui

from ..extended import ExtendedModule


class ReleasesModule(ExtendedModule):
    """Releases module for monitoring latest releases from multiple platforms."""

    @property
    def id(self) -> str:
        return "releases"

    @property
    def name(self) -> str:
        return "Releases"

    @property
    def icon(self) -> str:
        return "new_releases"

    @property
    def description(self) -> str:
        return "Monitor latest releases from GitHub, GitLab, Codeberg, and Docker Hub"

    @property
    def version(self) -> str:
        return "1.0.0"

    def _parse_repository(self, repo_string: str) -> dict[str, Any]:
        """Parse repository string to determine platform and components."""
        # GitHub: owner/repo
        if re.match(r'^[^/]+/[^/]+$', repo_string):
            return {
                "platform": "github",
                "owner": repo_string.split('/')[0],
                "repo": repo_string.split('/')[1],
                "original": repo_string
            }
        
        # GitLab: gitlab:owner/repo or gitlab.com/owner/repo
        elif repo_string.startswith('gitlab:') or 'gitlab.com/' in repo_string:
            if repo_string.startswith('gitlab:'):
                repo_path = repo_string[7:]
            else:
                repo_path = repo_string.split('gitlab.com/')[1]
            
            parts = repo_path.split('/')
            if len(parts) >= 2:
                return {
                    "platform": "gitlab",
                    "owner": parts[0],
                    "repo": parts[1],
                    "original": repo_string
                }
        
        # Codeberg: codeberg:owner/repo or codeberg.org/owner/repo
        elif repo_string.startswith('codeberg:') or 'codeberg.org/' in repo_string:
            if repo_string.startswith('codeberg:'):
                repo_path = repo_string[9:]
            else:
                repo_path = repo_string.split('codeberg.org/')[1]
            
            parts = repo_path.split('/')
            if len(parts) >= 2:
                return {
                    "platform": "codeberg",
                    "owner": parts[0],
                    "repo": parts[1],
                    "original": repo_string
                }
        
        # Docker Hub: docker:owner/repo or docker.io/owner/repo
        elif repo_string.startswith('docker:') or 'docker.io/' in repo_string:
            if repo_string.startswith('docker:'):
                repo_path = repo_string[6:]
            else:
                repo_path = repo_string.split('docker.io/')[1]
            
            parts = repo_path.split('/')
            if len(parts) >= 1:
                owner = parts[0] if len(parts) > 1 else "library"
                repo = parts[1] if len(parts) > 1 else parts[0]
                return {
                    "platform": "docker",
                    "owner": owner,
                    "repo": repo,
                    "original": repo_string
                }
        
        # Default to GitHub
        return {
            "platform": "github",
            "owner": repo_string.split('/')[0] if '/' in repo_string else repo_string,
            "repo": repo_string.split('/')[1] if '/' in repo_string else repo_string,
            "original": repo_string
        }

    def _fetch_github_release(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Fetch latest release from GitHub."""
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}/releases"
            with urlopen(url, timeout=10) as response:
                releases = json.loads(response.read().decode())
            
            if releases:
                release = releases[0]  # Latest release first
                return {
                    "title": f"{owner}/{repo} {release['tag_name']}",
                    "summary": release["name"] or release["tag_name"],
                    "link": release["html_url"],
                    "published": release["published_at"],
                    "platform": "GitHub",
                    "repository": f"{owner}/{repo}",
                    "tag_name": release["tag_name"],
                    "author": release["author"]["login"],
                    "draft": release["draft"],
                    "prerelease": release["prerelease"],
                    "assets": release.get("assets", []),
                    "body": release.get("body", "")[:500] + "..." if len(release.get("body", "")) > 500 else release.get("body", "")
                }
        except Exception as e:
            return {
                "title": f"Error fetching {owner}/{repo}",
                "summary": f"Failed to fetch releases: {str(e)}",
                "link": f"https://github.com/{owner}/{repo}",
                "published": datetime.now().isoformat(),
                "platform": "GitHub",
                "repository": f"{owner}/{repo}",
                "error": str(e)
            }

    def _fetch_gitlab_release(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Fetch latest release from GitLab."""
        try:
            # GitLab API URL
            project_path = f"{owner}%2F{repo}"
            url = f"https://gitlab.com/api/v4/projects/{project_path}/releases"
            with urlopen(url, timeout=10) as response:
                releases = json.loads(response.read().decode())
            
            if releases:
                release = releases[0]  # Latest release first
                return {
                    "title": f"{owner}/{repo} {release['tag_name']}",
                    "summary": release["name"] or release["tag_name"],
                    "link": release["_links"]["self"],
                    "published": release["released_at"],
                    "platform": "GitLab",
                    "repository": f"{owner}/{repo}",
                    "tag_name": release["tag_name"],
                    "author": release["author"]["name"],
                    "draft": False,  # GitLab doesn't have draft releases
                    "prerelease": False,  # GitLab doesn't have prereleases
                    "assets": release.get("assets", {}).get("links", []),
                    "body": release.get("description", "")[:500] + "..." if len(release.get("description", "")) > 500 else release.get("description", "")
                }
        except Exception as e:
            return {
                "title": f"Error fetching {owner}/{repo}",
                "summary": f"Failed to fetch releases: {str(e)}",
                "link": f"https://gitlab.com/{owner}/{repo}",
                "published": datetime.now().isoformat(),
                "platform": "GitLab",
                "repository": f"{owner}/{repo}",
                "error": str(e)
            }

    def _fetch_codeberg_release(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Fetch latest release from Codeberg (uses Gitea API)."""
        try:
            url = f"https://codeberg.org/api/v1/repos/{owner}/{repo}/releases"
            with urlopen(url, timeout=10) as response:
                releases = json.loads(response.read().decode())
            
            if releases:
                release = releases[0]  # Latest release first
                return {
                    "title": f"{owner}/{repo} {release['tag_name']}",
                    "summary": release["name"] or release["tag_name"],
                    "link": release["html_url"],
                    "published": release["published_at"],
                    "platform": "Codeberg",
                    "repository": f"{owner}/{repo}",
                    "tag_name": release["tag_name"],
                    "author": release["author"]["login"],
                    "draft": release["draft"],
                    "prerelease": release["prerelease"],
                    "assets": release.get("assets", []),
                    "body": release.get("body", "")[:500] + "..." if len(release.get("body", "")) > 500 else release.get("body", "")
                }
        except Exception as e:
            return {
                "title": f"Error fetching {owner}/{repo}",
                "summary": f"Failed to fetch releases: {str(e)}",
                "link": f"https://codeberg.org/{owner}/{repo}",
                "published": datetime.now().isoformat(),
                "platform": "Codeberg",
                "repository": f"{owner}/{repo}",
                "error": str(e)
            }

    def _fetch_docker_release(self, owner: str, repo: str) -> dict[str, Any] | None:
        """Fetch latest release from Docker Hub."""
        try:
            # Docker Hub API doesn't provide releases in the same way
            # We'll fetch the latest tag information
            url = f"https://hub.docker.com/v2/repositories/{owner}/{repo}/tags"
            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            if data.get("results"):
                tag = data["results"][0]  # Latest tag first
                return {
                    "title": f"{owner}/{repo} {tag['name']}",
                    "summary": f"Docker image tag: {tag['name']}",
                    "link": f"https://hub.docker.com/r/{owner}/{repo}",
                    "published": tag.get("last_updated", datetime.now().isoformat()),
                    "platform": "Docker Hub",
                    "repository": f"{owner}/{repo}",
                    "tag_name": tag["name"],
                    "author": owner,
                    "draft": False,
                    "prerelease": "rc" in tag["name"].lower() or "beta" in tag["name"].lower(),
                    "assets": [],
                    "body": f"Docker image size: {tag.get('full_size', 0) / 1024 / 1024:.1f} MB"
                }
        except Exception as e:
            return {
                "title": f"Error fetching {owner}/{repo}",
                "summary": f"Failed to fetch releases: {str(e)}",
                "link": f"https://hub.docker.com/r/{owner}/{repo}",
                "published": datetime.now().isoformat(),
                "platform": "Docker Hub",
                "repository": f"{owner}/{repo}",
                "error": str(e)
            }

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch latest releases from configured repositories."""
        repos = self.config.get("repositories", [
            "microsoft/vscode",
            "gitlab:gitlab-org/gitlab",
            "codeberg:forgejo/forgejo",
            "docker:library/nginx"
        ])

        all_releases = []

        for repo_string in repos:
            parsed = self._parse_repository(repo_string)
            platform = parsed["platform"]
            owner = parsed["owner"]
            repo = parsed["repo"]

            release_data = None

            if platform == "github":
                release_data = self._fetch_github_release(owner, repo)
            elif platform == "gitlab":
                release_data = self._fetch_gitlab_release(owner, repo)
            elif platform == "codeberg":
                release_data = self._fetch_codeberg_release(owner, repo)
            elif platform == "docker":
                release_data = self._fetch_docker_release(owner, repo)

            if release_data:
                all_releases.append({
                    "title": release_data["title"],
                    "summary": release_data["summary"],
                    "link": release_data["link"],
                    "published": release_data["published"],
                    "tags": ["release", platform.lower(), repo],
                    "extra": release_data
                })

        return all_releases

    def render(self) -> None:
        """Render the releases module UI."""
        releases = self.fetch()

        with ui.column().classes("w-full gap-3"):
            if not releases:
                ui.label("No releases found").classes("text-gray-500")
                return

            # Show only the first 3 releases in compact view
            for release in releases[:3]:
                extra = release.get("extra", {})

                with ui.card().classes("w-full p-3 cursor-pointer hover:shadow-md transition-shadow"):
                    with ui.column().classes("w-full gap-2"):
                        # Repository and tag
                        with ui.row().classes("w-full justify-between items-start"):
                            repo_name = extra.get("repository", "unknown")
                            platform = extra.get("platform", "unknown")

                            with ui.column().classes("gap-1"):
                                ui.label(f"{platform}").classes("text-xs font-semibold text-blue-600")
                                ui.label(repo_name).classes("text-sm font-semibold text-gray-600")
                                ui.label(release["title"]).classes("text-lg font-semibold")

                            # Release badges
                            with ui.row().classes("gap-1"):
                                if extra.get("draft"):
                                    ui.label("DRAFT").classes("text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded")
                                elif extra.get("prerelease"):
                                    ui.label("PRE-RELEASE").classes("text-xs bg-orange-200 text-orange-700 px-2 py-1 rounded")
                                else:
                                    ui.label("STABLE").classes("text-xs bg-green-200 text-green-700 px-2 py-1 rounded")

                        # Summary
                        if release.get("summary"):
                            ui.label(release["summary"]).classes("text-sm text-gray-600 line-clamp-2")

                        # Meta info
                        with ui.row().classes("w-full justify-between items-center text-xs text-gray-500"):
                            if extra.get("author"):
                                ui.label(f"by {extra['author']}")

                            if release.get("published"):
                                pub_date = datetime.fromisoformat(release["published"].replace("Z", "+00:00"))
                                ui.label(pub_date.strftime("%Y-%m-%d"))

    def render_detail(self) -> None:
        """Render detailed releases view."""
        releases = self.fetch()

        with ui.column().classes("w-full gap-6 max-w-4xl mx-auto"):
            ui.label("Latest Releases").classes("text-3xl font-bold text-center")

            # Header with repository count
            unique_repos = len(set(r.get("extra", {}).get("repository", "") for r in releases))
            ui.label(f"Monitoring {unique_repos} repositories").classes("text-gray-600 text-center")

            if not releases:
                ui.label("No releases found").classes("text-gray-500 text-center")
                return

            # Show all releases
            for release in releases:
                extra = release.get("extra", {})

                with ui.card().classes("w-full p-6"):
                    with ui.column().classes("w-full gap-4"):
                        # Header
                        with ui.row().classes("w-full justify-between items-start"):
                            with ui.column().classes("gap-2"):
                                repo_name = extra.get("repository", "unknown")
                                platform = extra.get("platform", "unknown")
                                
                                ui.label(f"{platform}").classes("text-sm font-semibold text-blue-600")
                                ui.label(repo_name).classes("text-lg font-semibold text-gray-600")
                                ui.label(release["title"]).classes("text-2xl font-bold")

                                if release.get("summary"):
                                    ui.label(release["summary"]).classes("text-lg text-gray-700")

                            # Release badges
                            with ui.column().classes("gap-2 items-end"):
                                if extra.get("draft"):
                                    ui.label("DRAFT").classes("text-sm bg-gray-200 text-gray-700 px-3 py-1 rounded-full")
                                elif extra.get("prerelease"):
                                    ui.label("PRE-RELEASE").classes("text-sm bg-orange-200 text-orange-700 px-3 py-1 rounded-full")
                                else:
                                    ui.label("STABLE").classes("text-sm bg-green-200 text-green-700 px-3 py-1 rounded-full")

                                ui.button(
                                    "View Release",
                                    on_click=lambda url=release["link"]: ui.navigate.to(url)
                                ).classes(
                                    "bg-blue-500 text-white hover:bg-blue-600 "
                                    "transition-colors duration-200"
                                ).props("target=_blank")

                        # Meta information
                        with ui.row().classes("w-full gap-4 text-sm text-gray-600"):
                            if extra.get("author"):
                                ui.label(f"👤 {extra['author']}")

                            if release.get("published"):
                                pub_date = datetime.fromisoformat(release["published"].replace("Z", "+00:00"))
                                ui.label(f"📅 {pub_date.strftime('%Y-%m-%d %H:%M')}")

                            # Assets count
                            assets = extra.get("assets", [])
                            if assets:
                                ui.label(f"📦 {len(assets)} assets")

                        # Release body
                        if extra.get("body"):
                            with ui.expansion("Release Notes").classes("w-full"):
                                ui.label(extra["body"]).classes("text-sm text-gray-700 whitespace-pre-wrap")

                        # Downloadable assets
                        assets = extra.get("assets", [])
                        if assets:
                            ui.label("Downloads:").classes("font-semibold text-sm mt-2")
                            with ui.column().classes("w-full gap-2 ml-4"):
                                for asset in assets[:5]:  # Show first 5 assets
                                    with ui.row().classes("w-full justify-between items-center p-2 hover:bg-gray-50 rounded"):
                                        asset_name = asset.get("name", asset.get("link", {}).get("name", "Unknown"))
                                        ui.label(asset_name).classes("text-sm")
                                        
                                        if asset.get("size"):
                                            ui.label(f"{asset['size'] / 1024 / 1024:.1f} MB").classes("text-xs text-gray-500")
                                        
                                        asset_url = asset.get("browser_download_url", asset.get("link", {}).get("url"))
                                        if asset_url:
                                            ui.button(
                                                "Download",
                                                on_click=lambda url=asset_url: ui.navigate.to(url)
                                            ).classes(
                                                "text-xs bg-green-500 text-white hover:bg-green-600 "
                                                "transition-colors duration-200"
                                            ).props("target=_blank dense")

                        # Error details
                        if extra.get("error"):
                            with ui.expansion("Error Details").classes("w-full"):
                                ui.label(extra["error"]).classes("text-sm text-red-600")