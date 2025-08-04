"""Version comparison and update checker."""

from .core import UpdateInfo, UpdateStatus, UpdateType


class VersionComparator:
    """Semantic version comparison utility."""

    @staticmethod
    def parse_version(version: str) -> tuple[int, ...]:
        """Parse version string into comparable tuple."""
        # Remove 'v' prefix and handle pre-release identifiers
        version = version.lower().lstrip("v")

        # Split into main version and pre-release
        main_part = version.split("-")[0]

        # Parse main version parts
        parts = []
        for part in main_part.split("."):
            try:
                parts.append(int(part))
            except ValueError:
                # Handle non-numeric parts (like 'beta1')
                parts.append(part)

        return tuple(parts)

    @staticmethod
    def compare_versions(version1: str, version2: str) -> int:
        """Compare two versions.

        Returns:
            1 if version1 > version2
            0 if version1 == version2
            -1 if version1 < version2
        """
        v1_parts = VersionComparator.parse_version(version1)
        v2_parts = VersionComparator.parse_version(version2)

        # Compare part by part
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1_part = v1_parts[i] if i < len(v1_parts) else 0
            v2_part = v2_parts[i] if i < len(v2_parts) else 0

            if isinstance(v1_part, int) and isinstance(v2_part, int):
                if v1_part > v2_part:
                    return 1
                elif v1_part < v2_part:
                    return -1
            else:
                # String comparison for non-numeric parts
                v1_str = str(v1_part)
                v2_str = str(v2_part)
                if v1_str > v2_str:
                    return 1
                elif v1_str < v2_str:
                    return -1

        return 0

    @staticmethod
    def get_update_type(current_version: str, new_version: str) -> UpdateType:
        """Determine update type based on version difference."""
        v1_parts = VersionComparator.parse_version(current_version)
        v2_parts = VersionComparator.parse_version(new_version)

        if len(v1_parts) >= 3 and len(v2_parts) >= 3:
            if v2_parts[0] > v1_parts[0]:
                return UpdateType.MAJOR
            elif v2_parts[1] > v1_parts[1]:
                return UpdateType.MINOR
            elif v2_parts[2] > v1_parts[2]:
                return UpdateType.PATCH

        return UpdateType.MAJOR  # Default to major for complex cases


class UpdateChecker:
    """Module update checker."""

    def __init__(self, update_source, update_policy):
        self.update_source = update_source
        self.update_policy = update_policy

    async def check_for_update(
        self, module_id: str, current_version: str
    ) -> UpdateInfo | None:
        """Check if update is available for a module."""
        try:
            # Get latest version from update source
            latest_version_info = await self.update_source.get_latest_version(
                module_id, current_version
            )

            if not latest_version_info:
                return None

            # Compare versions
            comparison = VersionComparator.compare_versions(
                latest_version_info.version, current_version
            )

            if comparison <= 0:
                return None  # No update available

            # Check if update type is allowed by policy
            if not self._is_update_allowed(latest_version_info.update_type):
                return None

            # Create update info
            update_info = UpdateInfo(
                module_id=module_id,
                current_version=current_version,
                latest_version=latest_version_info.version,
                update_type=latest_version_info.update_type,
                status=UpdateStatus.AVAILABLE,
                version_info=latest_version_info,
            )

            return update_info

        except Exception as e:
            # Log error but don't raise to prevent breaking the system
            print(f"Error checking update for {module_id}: {e}")
            return None

    def _is_update_allowed(self, update_type: UpdateType) -> bool:
        """Check if update type is allowed by policy."""
        if update_type == UpdateType.SECURITY:
            return True  # Security updates are always allowed

        return update_type.value in self.update_policy.update_types


class ModuleUpdateRegistry:
    """Registry for tracking module updates."""

    def __init__(self):
        self._modules: dict[str, dict] = {}
        self._update_sources: dict[str, object] = {}

    def register_module(self, module_id: str, module_info: dict) -> None:
        """Register a module for update checking."""
        self._modules[module_id] = module_info

    def register_update_source(self, source_type: str, source_instance: object) -> None:
        """Register an update source."""
        self._update_sources[source_type] = source_instance

    def get_module_info(self, module_id: str) -> dict | None:
        """Get module information."""
        return self._modules.get(module_id)

    def get_all_modules(self) -> dict[str, dict]:
        """Get all registered modules."""
        return self._modules.copy()

    def get_update_source(self, source_type: str) -> object | None:
        """Get update source by type."""
        return self._update_sources.get(source_type)

    def unregister_module(self, module_id: str) -> None:
        """Unregister a module."""
        if module_id in self._modules:
            del self._modules[module_id]

    def clear(self) -> None:
        """Clear all registered modules and sources."""
        self._modules.clear()
        self._update_sources.clear()
