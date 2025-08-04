"""Module update system architecture."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Protocol


class UpdateType(Enum):
    """Update type enumeration."""

    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    SECURITY = "security"


class UpdateStatus(Enum):
    """Update status enumeration."""

    AVAILABLE = "available"
    DOWNLOADING = "downloading"
    INSTALLING = "installing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"


@dataclass
class VersionInfo:
    """Version information."""

    version: str
    release_date: datetime
    changelog: str
    download_url: str
    checksum: str
    signature: str
    update_type: UpdateType
    size: int


@dataclass
class UpdateInfo:
    """Update information."""

    module_id: str
    current_version: str
    latest_version: str
    update_type: UpdateType
    status: UpdateStatus
    version_info: VersionInfo
    error_message: str | None = None


class UpdateSource(ABC):
    """Abstract base class for update sources."""

    @abstractmethod
    async def get_latest_version(
        self, module_id: str, current_version: str
    ) -> VersionInfo | None:
        """Get latest version information for a module."""
        pass

    @abstractmethod
    async def download_update(
        self, version_info: VersionInfo, download_path: str
    ) -> bool:
        """Download update package."""
        pass

    async def close(self):
        """Close resources (default no-op)."""
        pass


class UpdateValidator(Protocol):
    """Protocol for update validators."""

    async def verify_signature(self, file_path: str, signature: str) -> bool:
        """Verify file signature."""
        ...

    async def verify_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify file checksum."""
        ...


class UpdatePolicy:
    """Update policy configuration."""

    def __init__(self, config: dict[str, Any]):
        self.auto_update = config.get("auto_update", False)
        self.update_types = config.get("update_types", ["patch", "security"])
        self.check_interval = config.get("check_interval", 3600)  # seconds
        self.backup_before_update = config.get("backup_before_update", True)
        self.prerelease_updates = config.get("prerelease_updates", False)


class UpdateStorage(ABC):
    """Abstract base class for update storage."""

    @abstractmethod
    async def save_update_info(self, update_info: UpdateInfo) -> None:
        """Save update information."""
        pass

    @abstractmethod
    async def get_update_info(self, module_id: str) -> UpdateInfo | None:
        """Get update information for a module."""
        pass

    @abstractmethod
    async def get_all_update_info(self) -> list[UpdateInfo]:
        """Get all update information."""
        pass

    @abstractmethod
    async def delete_update_info(self, module_id: str) -> None:
        """Delete update information for a module."""
        pass


class UpdateNotifier(ABC):
    """Abstract base class for update notifications."""

    @abstractmethod
    async def notify_update_available(self, update_info: UpdateInfo) -> None:
        """Notify about available update."""
        pass

    @abstractmethod
    async def notify_update_progress(self, module_id: str, progress: float) -> None:
        """Notify about update progress."""
        pass

    @abstractmethod
    async def notify_update_completed(self, module_id: str, success: bool) -> None:
        """Notify about update completion."""
        pass


class DefaultUpdateNotifier(UpdateNotifier):
    """Default concrete implementation of UpdateNotifier."""

    async def notify_update_available(self, update_info: UpdateInfo) -> None:
        # Simple implementation: log or print
        print(
            f"Update available for {update_info.module_id}: {update_info.latest_version}"
        )

    async def notify_update_progress(self, module_id: str, progress: float) -> None:
        print(f"Update progress for {module_id}: {progress * 100:.1f}%")

    async def notify_update_completed(self, module_id: str, success: bool) -> None:
        status = "succeeded" if success else "failed"
        print(f"Update for {module_id} {status}")


class UpdateProgressCallback(Protocol):
    """Protocol for update progress callbacks."""

    def __call__(self, module_id: str, progress: float, message: str) -> None: ...
