"""Update source implementations."""

from datetime import datetime

import aiohttp
from loguru import logger

from .core import UpdateSource, UpdateType, VersionInfo


class GitHubUpdateSource(UpdateSource):
    """GitHub-based update source."""

    def __init__(self, repo_owner: str, repo_name: str, token: str | None = None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.token = token
        self.api_base = "https://api.github.com"
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None:
            headers = {}
            if self.token:
                headers["Authorization"] = f"token {self.token}"

            self.session = aiohttp.ClientSession(headers=headers)

        return self.session

    async def get_latest_version(
        self, module_id: str, current_version: str
    ) -> VersionInfo | None:
        """Get latest version from GitHub releases."""
        try:
            session = await self._get_session()

            # Get releases
            releases_url = (
                f"{self.api_base}/repos/{self.repo_owner}/{self.repo_name}/releases"
            )
            async with session.get(releases_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to get releases: {response.status}")
                    return None

                releases = await response.json()

            # Find the latest release
            latest_release = None
            for release in releases:
                if release.get("prerelease", False):
                    continue  # Skip pre-releases for now

                latest_release = release
                break

            if not latest_release:
                return None

            # Parse release date
            release_date = datetime.fromisoformat(
                latest_release["published_at"].replace("Z", "+00:00")
            )

            # Get update type
            update_type = self._determine_update_type(
                current_version, latest_release["tag_name"]
            )

            # Find download URL for the module
            download_url = self._find_download_url(latest_release, module_id)
            if not download_url:
                return None

            # Get checksum if available
            checksum = await self._get_checksum(latest_release, module_id)

            return VersionInfo(
                version=latest_release["tag_name"].lstrip("v"),
                release_date=release_date,
                changelog=latest_release.get("body", ""),
                download_url=download_url,
                checksum=checksum,
                signature="",  # GitHub doesn't provide signatures by default
                update_type=update_type,
                size=0,  # Will be filled during download
            )

        except Exception as e:
            logger.error(f"Error getting latest version from GitHub: {e}")
            return None

    def _find_download_url(self, release: dict, module_id: str) -> str | None:
        """Find download URL for a specific module."""
        assets = release.get("assets", [])

        # Look for module-specific asset
        for asset in assets:
            name = asset.get("name", "").lower()
            if module_id.lower() in name:
                return asset.get("browser_download_url")

        # Fallback to first asset
        if assets:
            return assets[0].get("browser_download_url")

        # Fallback to source code
        return release.get("zipball_url")

    async def _get_checksum(self, release: dict, module_id: str) -> str:
        """Get checksum for the release."""
        # This is a placeholder - in real implementation, you might:
        # 1. Look for checksum files in the release assets
        # 2. Download and verify checksums
        # 3. Return empty string if not available

        return ""

    def _determine_update_type(
        self, current_version: str, new_version: str
    ) -> UpdateType:
        """Determine update type from version difference."""
        from .checker import VersionComparator

        return VersionComparator.get_update_type(current_version, new_version)

    async def download_update(
        self, version_info: VersionInfo, download_path: str
    ) -> bool:
        """Download update from GitHub."""
        try:
            session = await self._get_session()

            async with session.get(version_info.download_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download update: {response.status}")
                    return False

                # Get file size
                # total_size = int(response.headers.get("content-length", 0))

                # Download file
                with open(download_path, "wb") as f:
                    downloaded = 0
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Update progress (could be used for progress reporting)
                        # progress = ((downloaded / total_size) * 100 if total_size > 0 else 0)

                # Update version info with actual size
                version_info.size = downloaded

                return True

        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            return False

    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None


class PyPIUpdateSource(UpdateSource):
    """PyPI-based update source."""

    def __init__(self, package_name: str):
        self.package_name = package_name
        self.api_base = "https://pypi.org/pypi"
        self.session = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        return self.session

    async def get_latest_version(
        self, module_id: str, current_version: str
    ) -> VersionInfo | None:
        """Get latest version from PyPI."""
        try:
            session = await self._get_session()

            # Get package info
            package_url = f"{self.api_base}/{self.package_name}/json"
            async with session.get(package_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to get package info: {response.status}")
                    return None

                package_info = await response.json()

            # Get latest version
            latest_version = package_info["info"]["version"]

            # Compare with current version
            from .checker import VersionComparator

            comparison = VersionComparator.compare_versions(
                latest_version, current_version
            )
            if comparison <= 0:
                return None

            # Get update type
            update_type = VersionComparator.get_update_type(
                current_version, latest_version
            )

            # Get release info
            releases = package_info.get("releases", {})
            release_info = releases.get(latest_version, [])

            if not release_info:
                return None

            # Find wheel or source distribution
            download_url = None
            size = 0
            checksum = ""

            for release in release_info:
                if release.get("packagetype") == "bdist_wheel":
                    download_url = release["url"]
                    size = release.get("size", 0)
                    checksum = release.get("digests", {}).get("sha256", "")
                    break

            if not download_url:
                # Fallback to source distribution
                for release in release_info:
                    if release.get("packagetype") == "sdist":
                        download_url = release["url"]
                        size = release.get("size", 0)
                        checksum = release.get("digests", {}).get("sha256", "")
                        break

            # Parse upload time
            upload_time = datetime.fromisoformat(
                release_info[0].get("upload_time", datetime.now().isoformat())
            )

            if download_url is None:
                return None

            return VersionInfo(
                version=latest_version,
                release_date=upload_time,
                changelog=package_info["info"].get("description", ""),
                download_url=download_url,
                checksum=checksum,
                signature="",
                update_type=update_type,
                size=size,
            )

        except Exception as e:
            logger.error(f"Error getting latest version from PyPI: {e}")
            return None

    async def download_update(
        self, version_info: VersionInfo, download_path: str
    ) -> bool:
        """Download update from PyPI."""
        try:
            session = await self._get_session()

            async with session.get(version_info.download_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download update: {response.status}")
                    return False

                # Download file
                with open(download_path, "wb") as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)

                return True

        except Exception as e:
            logger.error(f"Error downloading update: {e}")
            return False

    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None


class UpdateSourceManager:
    """Manager for update sources."""

    def __init__(self):
        self.sources: dict[str, UpdateSource] = {}

    def register_source(self, name: str, source: UpdateSource) -> None:
        """Register an update source."""
        self.sources[name] = source

    def get_source(self, name: str) -> UpdateSource | None:
        """Get update source by name."""
        return self.sources.get(name)

    def get_all_sources(self) -> dict[str, UpdateSource]:
        """Get all registered sources."""
        return self.sources.copy()

    async def close_all(self):
        """Close all update sources."""
        for source in self.sources.values():
            if hasattr(source, "close"):
                await source.close()

    def create_github_source(
        self, name: str, repo_owner: str, repo_name: str, token: str | None = None
    ) -> GitHubUpdateSource:
        """Create and register a GitHub update source."""
        source = GitHubUpdateSource(repo_owner, repo_name, token)
        self.register_source(name, source)
        return source

    def create_pypi_source(self, name: str, package_name: str) -> PyPIUpdateSource:
        """Create and register a PyPI update source."""
        source = PyPIUpdateSource(package_name)
        self.register_source(name, source)
        return source
