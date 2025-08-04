"""Storage implementation for update system."""

import json
from datetime import datetime
from pathlib import Path

from loguru import logger

from .core import UpdateInfo, UpdateStorage
import contextlib


class FileUpdateStorage(UpdateStorage):
    """File-based storage for update information."""

    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.updates_dir = self.storage_dir / "updates"
        self.history_dir = self.storage_dir / "history"
        self.updates_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    async def save_update_info(self, update_info: UpdateInfo) -> None:
        """Save update information to file."""
        try:
            file_path = self.updates_dir / f"{update_info.module_id}.json"

            data = {
                "module_id": update_info.module_id,
                "current_version": update_info.current_version,
                "latest_version": update_info.latest_version,
                "update_type": update_info.update_type.value,
                "status": update_info.status.value,
                "error_message": update_info.error_message,
                "version_info": {
                    "version": update_info.version_info.version,
                    "release_date": update_info.version_info.release_date.isoformat(),
                    "changelog": update_info.version_info.changelog,
                    "download_url": update_info.version_info.download_url,
                    "checksum": update_info.version_info.checksum,
                    "signature": update_info.version_info.signature,
                    "update_type": update_info.version_info.update_type.value,
                    "size": update_info.version_info.size,
                },
                "updated_at": datetime.now().isoformat(),
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving update info for {update_info.module_id}: {e}")
            raise

    async def get_update_info(self, module_id: str) -> UpdateInfo | None:
        """Get update information for a module."""
        try:
            file_path = self.updates_dir / f"{module_id}.json"

            if not file_path.exists():
                return None

            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            # Convert back to UpdateInfo
            from .core import UpdateStatus, UpdateType, VersionInfo

            version_info = VersionInfo(
                version=data["version_info"]["version"],
                release_date=datetime.fromisoformat(
                    data["version_info"]["release_date"]
                ),
                changelog=data["version_info"]["changelog"],
                download_url=data["version_info"]["download_url"],
                checksum=data["version_info"]["checksum"],
                signature=data["version_info"]["signature"],
                update_type=UpdateType(data["version_info"]["update_type"]),
                size=data["version_info"]["size"],
            )

            return UpdateInfo(
                module_id=data["module_id"],
                current_version=data["current_version"],
                latest_version=data["latest_version"],
                update_type=UpdateType(data["update_type"]),
                status=UpdateStatus(data["status"]),
                version_info=version_info,
                error_message=data.get("error_message"),
            )

        except Exception as e:
            logger.error(f"Error getting update info for {module_id}: {e}")
            return None

    async def get_all_update_info(self) -> list[UpdateInfo]:
        """Get all update information."""
        try:
            updates = []

            for file_path in self.updates_dir.glob("*.json"):
                try:
                    module_id = file_path.stem
                    update_info = await self.get_update_info(module_id)
                    if update_info:
                        updates.append(update_info)
                except Exception as e:
                    logger.error(f"Error loading update from {file_path}: {e}")

            return updates

        except Exception as e:
            logger.error(f"Error getting all update info: {e}")
            return []

    async def delete_update_info(self, module_id: str) -> None:
        """Delete update information for a module."""
        try:
            file_path = self.updates_dir / f"{module_id}.json"

            if file_path.exists():
                file_path.unlink()

        except Exception as e:
            logger.error(f"Error deleting update info for {module_id}: {e}")
            raise

    async def save_history_entry(self, entry: dict) -> None:
        """Save a history entry."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = self.history_dir / f"{timestamp}_{entry['module_id']}.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Error saving history entry: {e}")

    async def get_history_entries(self, limit: int = 100) -> list[dict]:
        """Get history entries."""
        try:
            entries = []

            # Get all history files, sorted by modification time
            history_files = sorted(
                self.history_dir.glob("*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )

            for file_path in history_files[:limit]:
                try:
                    with open(file_path, encoding="utf-8") as f:
                        entry = json.load(f)
                        entries.append(entry)
                except Exception as e:
                    logger.error(f"Error loading history from {file_path}: {e}")

            return entries

        except Exception as e:
            logger.error(f"Error getting history entries: {e}")
            return []

    async def cleanup_old_entries(self, days: int = 30) -> None:
        """Clean up old update entries."""
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)

            # Clean up old update info
            for file_path in self.updates_dir.glob("*.json"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"Cleaned up old update info: {file_path}")

            # Clean up old history entries
            for file_path in self.history_dir.glob("*.json"):
                if file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"Cleaned up old history entry: {file_path}")

        except Exception as e:
            logger.error(f"Error cleaning up old entries: {e}")


class MemoryUpdateStorage(UpdateStorage):
    """In-memory storage for update information."""

    def __init__(self):
        self._updates: dict[str, UpdateInfo] = {}
        self._history: list[dict] = []

    async def save_update_info(self, update_info: UpdateInfo) -> None:
        """Save update information to memory."""
        self._updates[update_info.module_id] = update_info

    async def get_update_info(self, module_id: str) -> UpdateInfo | None:
        """Get update information for a module."""
        return self._updates.get(module_id)

    async def get_all_update_info(self) -> list[UpdateInfo]:
        """Get all update information."""
        return list(self._updates.values())

    async def delete_update_info(self, module_id: str) -> None:
        """Delete update information for a module."""
        if module_id in self._updates:
            del self._updates[module_id]

    def add_history_entry(self, entry: dict) -> None:
        """Add a history entry."""
        self._history.append(entry)

    def get_history_entries(self, limit: int = 100) -> list[dict]:
        """Get history entries."""
        return self._history[-limit:]

    def clear(self) -> None:
        """Clear all data."""
        self._updates.clear()
        self._history.clear()


class UpdateNotifier:
    """Notifier for update events."""

    def __init__(self):
        self._callbacks: dict[str, list] = {
            "update_available": [],
            "update_progress": [],
            "update_completed": [],
            "update_error": [],
        }

    def register_callback(self, event_type: str, callback) -> None:
        """Register a callback for an event type."""
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)
        else:
            logger.warning(f"Unknown event type: {event_type}")

    def unregister_callback(self, event_type: str, callback) -> None:
        """Unregister a callback."""
        if event_type in self._callbacks:
            with contextlib.suppress(ValueError):
                self._callbacks[event_type].remove(callback)

    async def notify_update_available(self, update_info) -> None:
        """Notify about available update."""
        for callback in self._callbacks["update_available"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(update_info)
                else:
                    callback(update_info)
            except Exception as e:
                logger.error(f"Error in update_available callback: {e}")

    async def notify_update_progress(self, module_id: str, progress: float) -> None:
        """Notify about update progress."""
        for callback in self._callbacks["update_progress"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(module_id, progress)
                else:
                    callback(module_id, progress)
            except Exception as e:
                logger.error(f"Error in update_progress callback: {e}")

    async def notify_update_completed(self, module_id: str, success: bool) -> None:
        """Notify about update completion."""
        for callback in self._callbacks["update_completed"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(module_id, success)
                else:
                    callback(module_id, success)
            except Exception as e:
                logger.error(f"Error in update_completed callback: {e}")

    async def notify_update_error(self, module_id: str, error: str) -> None:
        """Notify about update error."""
        for callback in self._callbacks["update_error"]:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(module_id, error)
                else:
                    callback(module_id, error)
            except Exception as e:
                logger.error(f"Error in update_error callback: {e}")


# Import asyncio at the end to avoid circular imports
import asyncio
