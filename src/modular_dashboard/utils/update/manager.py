"""Update manager and executor."""

import asyncio
import contextlib
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from loguru import logger

from .checker import UpdateChecker
from .core import (
    UpdateInfo,
    UpdateNotifier,
    UpdatePolicy,
    UpdateProgressCallback,
    UpdateStatus,
    UpdateStorage,
)
from .sources import UpdateSourceManager


class UpdateExecutor:
    """Handles the actual execution of module updates."""

    def __init__(
        self,
        modules_dir: str,
        backup_dir: str,
        validator=None,
        progress_callback: UpdateProgressCallback | None = None,
    ):
        self.modules_dir = Path(modules_dir)
        self.backup_dir = Path(backup_dir)
        self.validator = validator
        self.progress_callback = progress_callback

        # Ensure directories exist
        self.modules_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    async def execute_update(self, update_info: UpdateInfo) -> bool:
        """Execute a module update."""
        try:
            module_id = update_info.module_id
            self._report_progress(module_id, 0.0, "Starting update")

            # Step 1: Backup current module
            if not await self._backup_module(module_id):
                self._report_progress(module_id, 0.0, "Backup failed")
                return False

            self._report_progress(module_id, 0.2, "Backup completed")

            # Step 2: Download update
            download_path = await self._download_update(update_info)
            if not download_path:
                self._report_progress(module_id, 0.2, "Download failed")
                return False

            self._report_progress(module_id, 0.5, "Download completed")

            # Step 3: Verify update
            if not await self._verify_update(download_path, update_info):
                self._report_progress(module_id, 0.5, "Verification failed")
                return False

            self._report_progress(module_id, 0.7, "Verification completed")

            # Step 4: Install update
            if not await self._install_update(module_id, download_path):
                self._report_progress(module_id, 0.7, "Installation failed")
                return False

            self._report_progress(module_id, 1.0, "Update completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error executing update for {module_id}: {e}")
            self._report_progress(module_id, 0.0, f"Update failed: {str(e)}")
            return False

    async def _backup_module(self, module_id: str) -> bool:
        """Backup current module."""
        try:
            module_path = self.modules_dir / module_id
            if not module_path.exists():
                logger.warning(f"Module {module_id} not found, skipping backup")
                return True

            # Create backup directory
            backup_path = (
                self.backup_dir
                / f"{module_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            backup_path.mkdir(parents=True, exist_ok=True)

            # Copy module files
            shutil.copytree(module_path, backup_path / module_id)

            logger.info(f"Module {module_id} backed up to {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Error backing up module {module_id}: {e}")
            return False

    async def _download_update(self, update_info: UpdateInfo) -> str | None:
        """Download update package."""
        try:
            # Create temporary directory
            temp_dir = tempfile.mkdtemp(prefix="modular_update_")
            download_path = os.path.join(
                temp_dir, f"{update_info.module_id}_update.zip"
            )

            # Download using update source
            # This is a placeholder - in real implementation, you'd use the update source
            # For now, we'll simulate the download
            logger.info(f"Downloading update for {update_info.module_id}")

            # Simulate download delay
            await asyncio.sleep(1)

            return download_path

        except Exception as e:
            logger.error(f"Error downloading update for {update_info.module_id}: {e}")
            return None

    async def _verify_update(self, download_path: str, update_info: UpdateInfo) -> bool:
        """Verify update package."""
        try:
            if not self.validator:
                logger.warning("No validator available, skipping verification")
                return True

            # Verify checksum
            if (
                update_info.version_info.checksum
                and not await self.validator.verify_checksum(
                    download_path, update_info.version_info.checksum
                )
            ):
                logger.error("Checksum verification failed")
                return False

            # Verify signature
            if (
                update_info.version_info.signature
                and not await self.validator.verify_signature(
                    download_path, update_info.version_info.signature
                )
            ):
                logger.error("Signature verification failed")
                return False

            return True

        except Exception as e:
            logger.error(f"Error verifying update: {e}")
            return False

    async def _install_update(self, module_id: str, download_path: str) -> bool:
        """Install update package."""
        try:
            module_path = self.modules_dir / module_id

            # Remove existing module
            if module_path.exists():
                shutil.rmtree(module_path)

            # Extract update package
            with zipfile.ZipFile(download_path, "r") as zip_ref:
                zip_ref.extractall(self.modules_dir)

            logger.info(f"Module {module_id} updated successfully")
            return True

        except Exception as e:
            logger.error(f"Error installing update for {module_id}: {e}")
            return False

    def _report_progress(self, module_id: str, progress: float, message: str) -> None:
        """Report update progress."""
        if self.progress_callback:
            self.progress_callback(module_id, progress, message)


class UpdateManager:
    """Main update manager that coordinates the update process."""

    def __init__(
        self,
        modules_dir: str,
        backup_dir: str,
        storage: UpdateStorage,
        notifier: UpdateNotifier,
        policy: UpdatePolicy,
    ):
        self.modules_dir = modules_dir
        self.backup_dir = backup_dir
        self.storage = storage
        self.notifier = notifier
        self.policy = policy

        # Initialize components
        self.source_manager = UpdateSourceManager()
        self.update_registry = None  # Will be set later
        self.executor = UpdateExecutor(modules_dir, backup_dir)

        # Background tasks
        self._check_task: asyncio.Task | None = None
        self._auto_update_task: asyncio.Task | None = None

        # State tracking
        self._active_updates: dict[str, UpdateInfo] = {}
        self._update_history: list[dict] = []

    def set_update_registry(self, registry) -> None:
        """Set the update registry."""
        self.update_registry = registry

    async def check_all_updates(self) -> list[UpdateInfo]:
        """Check for updates for all registered modules."""
        if not self.update_registry:
            logger.error("Update registry not set")
            return []

        updates = []
        modules = self.update_registry.get_all_modules()

        for module_id, module_info in modules.items():
            try:
                # Get update source for module
                source_type = module_info.get("update_source", "github")
                source = self.source_manager.get_source(source_type)

                if not source:
                    logger.warning(f"No update source found for {module_id}")
                    continue

                # Check for update
                checker = UpdateChecker(source, self.policy)
                update_info = await checker.check_for_update(
                    module_id, module_info.get("version", "1.0.0")
                )

                if update_info:
                    updates.append(update_info)
                    await self.storage.save_update_info(update_info)

                    # Notify about available update
                    await self.notifier.notify_update_available(update_info)

            except Exception as e:
                logger.error(f"Error checking update for {module_id}: {e}")

        return updates

    async def install_update(self, module_id: str) -> bool:
        """Install update for a specific module."""
        try:
            # Get update info
            update_info = await self.storage.get_update_info(module_id)
            if not update_info:
                logger.error(f"No update info found for {module_id}")
                return False

            # Update status
            update_info.status = UpdateStatus.INSTALLING
            await self.storage.save_update_info(update_info)

            # Track active update
            self._active_updates[module_id] = update_info

            # Execute update
            success = await self.executor.execute_update(update_info)

            # Update status and history
            update_info.status = (
                UpdateStatus.COMPLETED if success else UpdateStatus.FAILED
            )
            await self.storage.save_update_info(update_info)

            # Record in history
            self._update_history.append(
                {
                    "module_id": module_id,
                    "version": update_info.latest_version,
                    "success": success,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Remove from active updates
            if module_id in self._active_updates:
                del self._active_updates[module_id]

            # Notify about completion
            await self.notifier.notify_update_completed(module_id, success)

            return success

        except Exception as e:
            logger.error(f"Error installing update for {module_id}: {e}")
            return False

    async def start_background_checks(self) -> None:
        """Start background update checking."""
        if self._check_task and not self._check_task.done():
            logger.warning("Background check task already running")
            return

        self._check_task = asyncio.create_task(self._background_check_loop())
        logger.info("Started background update checking")

    async def stop_background_checks(self) -> None:
        """Stop background update checking."""
        if self._check_task:
            self._check_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._check_task
            self._check_task = None
            logger.info("Stopped background update checking")

    async def _background_check_loop(self) -> None:
        """Background loop for checking updates."""
        while True:
            try:
                await self.check_all_updates()
                await asyncio.sleep(self.policy.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in background check loop: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    async def start_auto_updates(self) -> None:
        """Start automatic updates."""
        if not self.policy.auto_update:
            logger.info("Auto-update disabled")
            return

        if self._auto_update_task and not self._auto_update_task.done():
            logger.warning("Auto-update task already running")
            return

        self._auto_update_task = asyncio.create_task(self._auto_update_loop())
        logger.info("Started automatic updates")

    async def stop_auto_updates(self) -> None:
        """Stop automatic updates."""
        if self._auto_update_task:
            self._auto_update_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._auto_update_task
            self._auto_update_task = None
            logger.info("Stopped automatic updates")

    async def _auto_update_loop(self) -> None:
        """Background loop for automatic updates."""
        while True:
            try:
                # Get available updates
                all_updates = await self.storage.get_all_update_info()

                # Filter updates that match policy
                eligible_updates = [
                    update
                    for update in all_updates
                    if (
                        update.status == UpdateStatus.AVAILABLE
                        and update.update_type.value in self.policy.update_types
                    )
                ]

                # Install updates
                for update in eligible_updates:
                    await self.install_update(update.module_id)
                    await asyncio.sleep(5)  # Small delay between updates

                await asyncio.sleep(self.policy.check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in auto-update loop: {e}")
                await asyncio.sleep(60)

    def get_update_history(self) -> list[dict]:
        """Get update history."""
        return self._update_history.copy()

    def get_active_updates(self) -> dict[str, UpdateInfo]:
        """Get currently active updates."""
        return self._active_updates.copy()

    async def shutdown(self) -> None:
        """Shutdown the update manager."""
        await self.stop_background_checks()
        await self.stop_auto_updates()
        await self.source_manager.close_all()
