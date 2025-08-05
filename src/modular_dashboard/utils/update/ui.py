"""Update UI components for NiceGUI."""

from loguru import logger
from nicegui import ui

from .core import UpdateInfo, UpdateStatus, UpdateType
from .manager import UpdateManager


class UpdateUI:
    """UI components for module updates."""

    def __init__(self, update_manager: UpdateManager):
        self.update_manager = update_manager
        self.current_updates: dict[str, UpdateInfo] = {}
        self.update_list_container = None
        self.settings_container = None
        self.history_container = None

    def render_update_panel(self) -> None:
        """Render the main update panel."""
        with ui.card().classes("w-full p-4"):
            ui.label("模块更新管理").classes("text-lg font-semibold mb-4")

            # Settings section
            self._render_settings_section()

            # Action buttons
            self._render_action_buttons()

            # Updates list
            self._render_updates_list()

            # Update history
            self._render_update_history()

    def _render_settings_section(self) -> None:
        """Render update settings section."""
        with (
            ui.expansion("更新设置", icon="settings").classes("w-full mb-4"),
            ui.column().classes("w-full gap-4 p-4"),
            ui.column().classes("w-full gap-4 p-4"),
        ):
            # Auto-update toggle
            ui.switch(
                "自动更新",
                value=self.update_manager.policy.auto_update,
                on_change=lambda e: self._update_policy("auto_update", e.value),
            ).classes("w-full")

            # Update types
            ui.label("更新类型").classes("text-sm font-medium")
            with ui.row().classes("w-full gap-2"):
                ui.checkbox(
                    "补丁更新",
                    value="patch" in self.update_manager.policy.update_types,
                    on_change=lambda e: self._toggle_update_type("patch", e.value),
                )
                ui.checkbox(
                    "次要更新",
                    value="minor" in self.update_manager.policy.update_types,
                    on_change=lambda e: self._toggle_update_type("minor", e.value),
                )
                ui.checkbox(
                    "主要更新",
                    value="major" in self.update_manager.policy.update_types,
                    on_change=lambda e: self._toggle_update_type("major", e.value),
                )
                ui.checkbox(
                    "安全更新",
                    value="security" in self.update_manager.policy.update_types,
                    on_change=lambda e: self._toggle_update_type("security", e.value),
                )

                # Check interval
                with ui.row().classes("w-full gap-4 items-center"):
                    ui.label("检查间隔(小时):").classes("text-sm")
                    ui.number(
                        value=self.update_manager.policy.check_interval / 3600,
                        min=1,
                        max=168,
                        step=1,
                        on_change=lambda e: self._update_policy(
                            "check_interval", e.value * 3600
                        ),
                    ).classes("w-24")

    def _render_action_buttons(self) -> None:
        """Render action buttons."""
        with ui.row().classes("w-full gap-2 mb-4"):
            ui.button("检查更新", icon="refresh", on_click=self._check_updates).classes(
                "bg-blue-500 text-white"
            )

            ui.button(
                "安装所有更新", icon="system_update", on_click=self._install_all_updates
            ).classes("bg-green-500 text-white")

            if self.update_manager.policy.auto_update:
                ui.button(
                    "停止自动更新", icon="pause", on_click=self._stop_auto_updates
                ).classes("bg-orange-500 text-white")
            else:
                ui.button(
                    "启动自动更新", icon="play_arrow", on_click=self._start_auto_updates
                ).classes("bg-green-500 text-white")

    def _render_updates_list(self) -> None:
        """Render the updates list."""
        with ui.card().classes("w-full p-4"):
            ui.label("可用更新").classes("text-lg font-semibold mb-4")

            self.update_list_container = ui.column().classes("w-full gap-2")

            # Load initial updates
            self._refresh_updates_list()

    def _render_update_history(self) -> None:
        """Render update history."""
        with ui.expansion("更新历史", icon="history").classes("w-full mt-4"):
            self.history_container = ui.column().classes("w-full gap-2 p-4")

            # Load initial history
            self._refresh_update_history()

    def _refresh_updates_list(self) -> None:
        """Refresh the updates list."""
        if not self.update_list_container:
            return

        # Clear existing content
        self.update_list_container.clear()

        # Get current updates
        with self.update_list_container:
            if not self.current_updates:
                ui.label("没有可用的更新").classes("text-gray-500 text-center py-4")
                return

            for module_id, update_info in self.current_updates.items():
                self._render_update_item(module_id, update_info)

    def _render_update_item(self, module_id: str, update_info: UpdateInfo) -> None:
        """Render a single update item."""
        with (
            ui.card().classes("w-full p-3"),
            ui.row().classes("w-full justify-between items-center"),
        ):
            # Module info
            with ui.column().classes("flex-1"):
                with ui.row().classes("w-full justify-between items-center"):
                    ui.label(f"{module_id}").classes("font-semibold")
                    self._render_update_type_badge(update_info.update_type)

                with ui.row().classes("w-full gap-4 text-sm text-gray-600"):
                    ui.label(f"当前版本: {update_info.current_version}")
                    ui.label("→")
                    ui.label(f"最新版本: {update_info.latest_version}")

                if update_info.version_info.changelog:
                    with ui.expansion("更新日志", icon="description").classes("w-full"):
                        ui.markdown(update_info.version_info.changelog).classes(
                            "text-sm"
                        )

            # Actions
            with ui.column().classes("gap-2"):
                if update_info.status == UpdateStatus.AVAILABLE:
                    ui.button(
                        "安装",
                        icon="download",
                        on_click=lambda _: self._install_update(module_id),
                    ).classes("bg-green-500 text-white")
                elif update_info.status == UpdateStatus.INSTALLING:
                    ui.button("安装中...", icon="hourglass_top").props("disable")
                elif update_info.status == UpdateStatus.COMPLETED:
                    ui.button("已完成", icon="check_circle").props("disable")
                elif update_info.status == UpdateStatus.FAILED:
                    ui.button("失败", icon="error").classes("bg-red-500 text-white")

    def _render_update_type_badge(self, update_type: UpdateType) -> None:
        """Render update type badge."""
        colors = {
            UpdateType.MAJOR: "bg-red-500",
            UpdateType.MINOR: "bg-yellow-500",
            UpdateType.PATCH: "bg-green-500",
            UpdateType.SECURITY: "bg-purple-500",
        }

        labels = {
            UpdateType.MAJOR: "主要更新",
            UpdateType.MINOR: "次要更新",
            UpdateType.PATCH: "补丁更新",
            UpdateType.SECURITY: "安全更新",
        }

        color = colors.get(update_type, "bg-gray-500")
        label = labels.get(update_type, "未知")

        ui.label(label).classes(f"text-white text-xs px-2 py-1 rounded {color}")

    def _refresh_update_history(self) -> None:
        """Refresh update history."""
        if not self.history_container:
            return

        # Clear existing content
        self.history_container.clear()

        # Get history
        history = self.update_manager.get_update_history()

        with self.history_container:
            if not history:
                ui.label("暂无更新历史").classes("text-gray-500 text-center py-4")
                return

            for entry in history:
                self._render_history_entry(entry)

    def _render_history_entry(self, entry: dict) -> None:
        """Render a single history entry."""
        with (
            ui.card().classes("w-full p-3"),
            ui.row().classes("w-full justify-between items-center"),
        ):
            with ui.column().classes("flex-1"):
                ui.label(f"{entry['module_id']}").classes("font-semibold")
                ui.label(f"版本: {entry['version']}").classes("text-sm text-gray-600")
                ui.label(f"时间: {entry['timestamp']}").classes("text-sm text-gray-500")

            # Status
            if entry["success"]:
                ui.label("成功").classes("text-green-600 text-sm")
            else:
                ui.label("失败").classes("text-red-600 text-sm")

    async def _check_updates(self) -> None:
        """Check for updates."""
        try:
            ui.notify("正在检查更新...", type="info")

            # Check updates
            updates = await self.update_manager.check_all_updates()

            # Update current updates
            self.current_updates = {u.module_id: u for u in updates}

            # Refresh UI
            self._refresh_updates_list()

            if updates:
                ui.notify(f"发现 {len(updates)} 个更新", type="positive")
            else:
                ui.notify("没有发现更新", type="info")

        except Exception as e:
            logger.error(f"Error checking updates: {e}")
            ui.notify(f"检查更新失败: {str(e)}", type="negative")

    async def _install_update(self, module_id: str) -> None:
        """Install update for a specific module."""
        try:
            ui.notify(f"正在安装 {module_id} 的更新...", type="info")

            # Install update
            success = await self.update_manager.install_update(module_id)

            if success:
                ui.notify(f"{module_id} 更新成功", type="positive")
                # Refresh updates list
                await self._check_updates()
            else:
                ui.notify(f"{module_id} 更新失败", type="negative")

        except Exception as e:
            logger.error(f"Error installing update: {e}")
            ui.notify(f"安装更新失败: {str(e)}", type="negative")

    async def _install_all_updates(self) -> None:
        """Install all available updates."""
        try:
            available_updates = [
                u
                for u in self.current_updates.values()
                if u.status == UpdateStatus.AVAILABLE
            ]

            if not available_updates:
                ui.notify("没有可安装的更新", type="info")
                return

            ui.notify(f"正在安装 {len(available_updates)} 个更新...", type="info")

            # Install updates
            for update_info in available_updates:
                await self.update_manager.install_update(update_info.module_id)

            ui.notify("批量更新完成", type="positive")

            # Refresh updates list
            await self._check_updates()

        except Exception as e:
            logger.error(f"Error installing all updates: {e}")
            ui.notify(f"批量更新失败: {str(e)}", type="negative")

    async def _start_auto_updates(self) -> None:
        """Start automatic updates."""
        try:
            await self.update_manager.start_auto_updates()
            ui.notify("自动更新已启动", type="positive")
        except Exception as e:
            logger.error(f"Error starting auto updates: {e}")
            ui.notify(f"启动自动更新失败: {str(e)}", type="negative")

    async def _stop_auto_updates(self) -> None:
        """Stop automatic updates."""
        try:
            await self.update_manager.stop_auto_updates()
            ui.notify("自动更新已停止", type="positive")
        except Exception as e:
            logger.error(f"Error stopping auto updates: {e}")
            ui.notify(f"停止自动更新失败: {str(e)}", type="negative")

    def _update_policy(self, key: str, value) -> None:
        """Update policy setting."""
        setattr(self.update_manager.policy, key, value)
        ui.notify("设置已更新", type="positive")

    def _toggle_update_type(self, update_type: str, enabled: bool) -> None:
        """Toggle update type in policy."""
        if enabled:
            if update_type not in self.update_manager.policy.update_types:
                self.update_manager.policy.update_types.append(update_type)
        else:
            if update_type in self.update_manager.policy.update_types:
                self.update_manager.policy.update_types.remove(update_type)

        ui.notify("更新类型设置已更新", type="positive")
        self._refresh_updates_list()

    def show_update_dialog(self, update_info: UpdateInfo) -> None:
        """Show update details dialog."""
        with ui.dialog() as dialog, ui.card():
            ui.label(f"更新详情: {update_info.module_id}").classes(
                "text-lg font-semibold mb-4"
            )

            with ui.column().classes("w-full gap-2"):
                ui.label(f"当前版本: {update_info.current_version}")
                ui.label(f"最新版本: {update_info.latest_version}")
                ui.label(f"更新类型: {update_info.update_type.value}")

                if update_info.version_info.changelog:
                    ui.label("更新日志:").classes("font-semibold")
                    ui.markdown(update_info.version_info.changelog).classes("text-sm")

                with ui.row().classes("w-full gap-2"):
                    ui.button(
                        "安装",
                        on_click=lambda: self._install_update(update_info.module_id),
                    ).classes("bg-green-500 text-white")
                    ui.button("关闭", on_click=dialog.close)


class UpdateProgressDialog:
    """Progress dialog for update operations."""

    def __init__(self):
        self.dialog = None
        self.progress_bar = None
        self.status_label = None
        self.module_label = None

    def show(self, module_id: str, title: str = "正在更新") -> None:
        """Show progress dialog."""
        self.dialog = ui.dialog()

        with self.dialog, ui.card().classes("w-96"):
            ui.label(title).classes("text-lg font-semibold mb-4")

            self.module_label = ui.label(f"模块: {module_id}").classes("text-sm mb-2")

            self.progress_bar = ui.linear_progress(value=0).classes("w-full mb-2")

            self.status_label = ui.label("准备中...").classes("text-sm text-gray-600")

            ui.button("取消", on_click=self.hide).classes("mt-4")

        self.dialog.open()

    def update_progress(self, progress: float, message: str) -> None:
        """Update progress."""
        if self.progress_bar:
            self.progress_bar.props(f"value={progress}")

        if self.status_label:
            self.status_label.text = message

    def hide(self) -> None:
        """Hide progress dialog."""
        if self.dialog:
            self.dialog.close()
            self.dialog = None
