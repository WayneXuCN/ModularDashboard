"""System monitoring module for real-time resource monitoring."""

import asyncio
import contextlib
import platform
import socket
import subprocess
from collections.abc import Callable
from datetime import datetime
from typing import Any

import psutil
from nicegui import ui

from ...ui.styles import DashboardStyles
from ..extended import ExtendedModule


class SystemMonitorModule(ExtendedModule):
    """System monitoring module for real-time resource monitoring."""

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self._monitoring_task: asyncio.Task | None = None
        self._current_data: dict[str, Any] = {}
        self._alert_states: dict[str, bool] = {}
        self._alert_callbacks: list[Callable] = []

    @property
    def id(self) -> str:
        return "system_monitor"

    @property
    def name(self) -> str:
        return "System Monitor"

    @property
    def icon(self) -> str:
        return "computer"

    @property
    def description(self) -> str:
        return "Real-time system resource monitoring with alerts"

    @property
    def version(self) -> str:
        return "1.0.0"

    def has_cache(self) -> bool:
        return True

    def get_default_config(self) -> dict[str, Any]:
        """Get default configuration for system monitoring."""
        return {
            "refresh_interval": 2,  # seconds
            "enable_cpu": True,
            "enable_memory": True,
            "enable_disk": True,
            "enable_network": True,
            "enable_temperature": True,
            "enable_gpu": True,
            "disk_paths": ["/"],  # Default paths to monitor
            "network_interfaces": [],  # Empty means all interfaces
            "alerts": {
                "cpu_percent": 80,  # Alert threshold
                "memory_percent": 85,
                "disk_percent": 90,
                "temperature_celsius": 70,
            },
            "ui": {
                "show_charts": True,
                "show_details": True,
                "compact_view": False,
                "theme": "auto",  # auto, light, dark
            },
        }

    def _get_cpu_info(self) -> dict[str, Any]:
        """Get CPU information."""
        if not self.config.get("enable_cpu", True):
            return {}

        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            cpu_count_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()

            # Get per-core CPU usage
            cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)

            # Load average (Unix only)
            load_avg = None
            if hasattr(psutil, "getloadavg"):
                with contextlib.suppress(OSError, AttributeError):
                    load_avg = psutil.getloadavg()

            return {
                "percent": cpu_percent,
                "count": cpu_count,
                "count_logical": cpu_count_logical,
                "frequency": {
                    "current": cpu_freq.current if cpu_freq else 0,
                    "min": cpu_freq.min if cpu_freq else 0,
                    "max": cpu_freq.max if cpu_freq else 0,
                },
                "per_core": cpu_per_core,
                "load_average": load_avg,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_memory_info(self) -> dict[str, Any]:
        """Get memory information."""
        if not self.config.get("enable_memory", True):
            return {}

        try:
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()

            return {
                "virtual": {
                    "total": virtual_memory.total,
                    "available": virtual_memory.available,
                    "used": virtual_memory.used,
                    "free": virtual_memory.free,
                    "percent": virtual_memory.percent,
                    "active": getattr(virtual_memory, "active", None),
                    "inactive": getattr(virtual_memory, "inactive", None),
                    "buffers": getattr(virtual_memory, "buffers", None),
                    "cached": getattr(virtual_memory, "cached", None),
                },
                "swap": {
                    "total": swap_memory.total,
                    "used": swap_memory.used,
                    "free": swap_memory.free,
                    "percent": swap_memory.percent,
                    "sin": swap_memory.sin,
                    "sout": swap_memory.sout,
                },
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    def _get_disk_info(self) -> dict[str, Any]:
        """Get disk information."""
        if not self.config.get("enable_disk", True):
            return {}

        try:
            disk_info = {}
            disk_paths = self.config.get("disk_paths", ["/"])

            for path in disk_paths:
                try:
                    disk_usage = psutil.disk_usage(path)
                    disk_io = psutil.disk_io_counters()

                    disk_info[path] = {
                        "usage": {
                            "total": disk_usage.total,
                            "used": disk_usage.used,
                            "free": disk_usage.free,
                            "percent": disk_usage.percent,
                        },
                        "io": {
                            "read_count": disk_io.read_count if disk_io else 0,
                            "write_count": disk_io.write_count if disk_io else 0,
                            "read_bytes": disk_io.read_bytes if disk_io else 0,
                            "write_bytes": disk_io.write_bytes if disk_io else 0,
                            "read_time": disk_io.read_time if disk_io else 0,
                            "write_time": disk_io.write_time if disk_io else 0,
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                except Exception as e:
                    disk_info[path] = {"error": str(e)}

            # Also get all disk partitions
            try:
                partitions = []
                for part in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(part.mountpoint)
                        partitions.append(
                            {
                                "device": part.device,
                                "mountpoint": part.mountpoint,
                                "fstype": part.fstype,
                                "total": usage.total,
                                "used": usage.used,
                                "free": usage.free,
                                "percent": usage.percent,
                            }
                        )
                    except PermissionError:
                        continue

                disk_info["partitions"] = partitions
            except Exception as e:
                disk_info["partitions_error"] = str(e)

            return disk_info
        except Exception as e:
            return {"error": str(e)}

    def _get_network_info(self) -> dict[str, Any]:
        """Get network information."""
        if not self.config.get("enable_network", True):
            return {}

        try:
            net_io = psutil.net_io_counters(pernic=True)
            interfaces = self.config.get("network_interfaces", [])

            network_info = {}
            for interface, stats in net_io.items():
                if interfaces and interface not in interfaces:
                    continue

                try:
                    # Get interface addresses
                    addrs = psutil.net_if_addrs().get(interface, [])
                    ipv4 = None
                    ipv6 = None
                    mac = None

                    for addr in addrs:
                        if addr.family == socket.AF_INET:
                            ipv4 = addr.address
                        elif addr.family == socket.AF_INET6:
                            ipv6 = addr.address
                        elif addr.family == psutil.AF_LINK:
                            mac = addr.address

                    network_info[interface] = {
                        "bytes_sent": stats.bytes_sent,
                        "bytes_recv": stats.bytes_recv,
                        "packets_sent": stats.packets_sent,
                        "packets_recv": stats.packets_recv,
                        "errin": stats.errin,
                        "errout": stats.errout,
                        "dropin": stats.dropin,
                        "dropout": stats.dropout,
                        "addresses": {
                            "ipv4": ipv4,
                            "ipv6": ipv6,
                            "mac": mac,
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                except Exception as e:
                    network_info[interface] = {"error": str(e)}

            return network_info
        except Exception as e:
            return {"error": str(e)}

    def _get_temperature_info(self) -> dict[str, Any]:
        """Get temperature information."""
        if not self.config.get("enable_temperature", True):
            return {}

        try:
            temp_info = {}

            sensors_temperatures = getattr(psutil, "sensors_temperatures", None)
            if callable(sensors_temperatures):
                temps = sensors_temperatures()
                if isinstance(temps, dict):
                    for name, entries in temps.items():
                        for entry in entries:
                            temp_info[f"{name}_{entry.label or 'default'}"] = {
                                "current": entry.current,
                                "high": entry.high,
                                "critical": entry.critical,
                                "label": entry.label,
                                "timestamp": datetime.now().isoformat(),
                            }

            return temp_info
        except Exception as e:
            return {"error": str(e)}

    def _get_gpu_info(self) -> dict[str, Any]:
        """Get GPU information."""
        if not self.config.get("enable_gpu", True):
            return {}

        try:
            gpu_info = {}

            # Try to get GPU information using nvidia-ml-py if available
            try:
                import pynvml

                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()

                for i in range(device_count):
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    name = pynvml.nvmlDeviceGetName(handle)

                    # Get GPU memory info
                    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)

                    # Get GPU utilization
                    try:
                        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                        gpu_util = utilization.gpu
                        memory_util = utilization.memory
                    except pynvml.NVMLError:
                        gpu_util = memory_util = 0

                    # Get temperature
                    try:
                        temp = pynvml.nvmlDeviceGetTemperature(
                            handle, pynvml.NVML_TEMPERATURE_GPU
                        )
                    except pynvml.NVMLError:
                        temp = 0

                    gpu_info[f"gpu_{i}"] = {
                        "name": name,
                        "memory": {
                            "total": memory_info.total,
                            "used": memory_info.used,
                            "free": memory_info.free,
                            "percent": (
                                (memory_info.used / memory_info.total) * 100
                                if isinstance(memory_info.used, int | float)
                                and isinstance(memory_info.total, int | float)
                                and memory_info.total
                                else 0
                            ),
                        },
                        "utilization": {
                            "gpu": gpu_util,
                            "memory": memory_util,
                        },
                        "temperature": temp,
                        "timestamp": datetime.now().isoformat(),
                    }

                pynvml.nvmlShutdown()
            except ImportError:
                # nvidia-ml-py not available
                pass
            except Exception:
                # NVIDIA GPU not available or error
                pass

            # Try AMD GPU detection
            try:
                # Check for AMD GPUs using subprocess
                result = subprocess.run(
                    ["rocm-smi", "--showproductname"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    gpu_info["amd_gpu"] = {
                        "type": "AMD",
                        "info": result.stdout,
                        "timestamp": datetime.now().isoformat(),
                    }
            except Exception:
                pass

            return gpu_info if gpu_info else {"error": "No GPU detected"}
        except Exception as e:
            return {"error": str(e)}

    def _get_system_info(self) -> dict[str, Any]:
        """Get general system information."""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            return {
                "system": {
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "processor": platform.processor(),
                    "hostname": platform.node(),
                    "boot_time": boot_time.isoformat(),
                    "uptime_seconds": (datetime.now() - boot_time).total_seconds(),
                },
                "processes": {
                    "count": len(psutil.pids()),
                    "running": sum(
                        1
                        for p in psutil.process_iter(["status"])
                        if p.info["status"] == "running"
                    ),
                },
                "users": [
                    {
                        "name": user.name,
                        "terminal": user.terminal,
                        "host": user.host,
                        "started": datetime.fromtimestamp(user.started).isoformat(),
                    }
                    for user in psutil.users()
                ],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": str(e)}

    def _check_alerts(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check for alert conditions."""
        alerts = {}
        alert_config = self.config.get("alerts", {})

        # Check CPU alerts
        if "cpu" in data and "percent" in data["cpu"]:
            cpu_percent = data["cpu"]["percent"]
            cpu_threshold = alert_config.get("cpu_percent", 80)
            if cpu_percent > cpu_threshold:
                alerts["cpu"] = {
                    "type": "warning",
                    "message": f"CPU usage high: {cpu_percent:.1f}%",
                    "value": cpu_percent,
                    "threshold": cpu_threshold,
                }

        # Check memory alerts
        if "memory" in data and "virtual" in data["memory"]:
            memory_percent = data["memory"]["virtual"]["percent"]
            memory_threshold = alert_config.get("memory_percent", 85)
            if memory_percent > memory_threshold:
                alerts["memory"] = {
                    "type": "warning",
                    "message": f"Memory usage high: {memory_percent:.1f}%",
                    "value": memory_percent,
                    "threshold": memory_threshold,
                }

        # Check disk alerts
        if "disk" in data:
            disk_threshold = alert_config.get("disk_percent", 90)
            for path, disk_data in data["disk"].items():
                if isinstance(disk_data, dict) and "usage" in disk_data:
                    disk_percent = disk_data["usage"]["percent"]
                    if disk_percent > disk_threshold:
                        alerts[f"disk_{path}"] = {
                            "type": "warning",
                            "message": f"Disk {path} usage high: {disk_percent:.1f}%",
                            "value": disk_percent,
                            "threshold": disk_threshold,
                        }

        # Check temperature alerts
        if "temperature" in data:
            temp_threshold = alert_config.get("temperature_celsius", 70)
            for sensor, temp_data in data["temperature"].items():
                if isinstance(temp_data, dict) and "current" in temp_data:
                    current_temp = temp_data["current"]
                    if current_temp > temp_threshold:
                        alerts[f"temp_{sensor}"] = {
                            "type": "warning",
                            "message": f"Temperature high: {current_temp:.1f}°C",
                            "value": current_temp,
                            "threshold": temp_threshold,
                        }

        return alerts

    def collect_system_data(self) -> dict[str, Any]:
        """Collect all system monitoring data."""
        data = {
            "cpu": self._get_cpu_info(),
            "memory": self._get_memory_info(),
            "disk": self._get_disk_info(),
            "network": self._get_network_info(),
            "temperature": self._get_temperature_info(),
            "gpu": self._get_gpu_info(),
            "system": self._get_system_info(),
        }

        # Check for alerts
        data["alerts"] = self._check_alerts(data)

        return data

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch system monitoring data."""
        data = self.collect_system_data()

        # Store current data for UI updates
        self._current_data = data

        # Create summary items for the dashboard
        items = []

        # CPU summary
        if "cpu" in data and "percent" in data["cpu"]:
            cpu_percent = data["cpu"]["percent"]
            items.append(
                {
                    "title": f"CPU: {cpu_percent:.1f}%",
                    "summary": f"Cores: {data['cpu'].get('count', 'N/A')} | Load: {data['cpu'].get('load_average', ['N/A'])[0] if data['cpu'].get('load_average') else 'N/A'}",
                    "link": None,
                    "published": datetime.now().isoformat(),
                    "tags": ["system", "cpu", "monitoring"],
                    "extra": {
                        "type": "cpu",
                        "data": data["cpu"],
                        "alert": "cpu" in data.get("alerts", {}),
                    },
                }
            )

        # Memory summary
        if "memory" in data and "virtual" in data["memory"]:
            memory_percent = data["memory"]["virtual"]["percent"]
            memory_used_gb = data["memory"]["virtual"]["used"] / (1024**3)
            memory_total_gb = data["memory"]["virtual"]["total"] / (1024**3)

            items.append(
                {
                    "title": f"Memory: {memory_percent:.1f}%",
                    "summary": f"{memory_used_gb:.1f}GB / {memory_total_gb:.1f}GB used",
                    "link": None,
                    "published": datetime.now().isoformat(),
                    "tags": ["system", "memory", "monitoring"],
                    "extra": {
                        "type": "memory",
                        "data": data["memory"],
                        "alert": "memory" in data.get("alerts", {}),
                    },
                }
            )

        # Disk summary
        if "disk" in data:
            for path, disk_data in data["disk"].items():
                if isinstance(disk_data, dict) and "usage" in disk_data:
                    disk_percent = disk_data["usage"]["percent"]
                    disk_used_gb = disk_data["usage"]["used"] / (1024**3)
                    disk_total_gb = disk_data["usage"]["total"] / (1024**3)

                    items.append(
                        {
                            "title": f"Disk {path}: {disk_percent:.1f}%",
                            "summary": f"{disk_used_gb:.1f}GB / {disk_total_gb:.1f}GB used",
                            "link": None,
                            "published": datetime.now().isoformat(),
                            "tags": ["system", "disk", "monitoring"],
                            "extra": {
                                "type": "disk",
                                "path": path,
                                "data": disk_data,
                                "alert": f"disk_{path}" in data.get("alerts", {}),
                            },
                        }
                    )

        # Network summary
        if "network" in data:
            total_bytes_sent = sum(
                net.get("bytes_sent", 0)
                for net in data["network"].values()
                if isinstance(net, dict)
            )
            total_bytes_recv = sum(
                net.get("bytes_recv", 0)
                for net in data["network"].values()
                if isinstance(net, dict)
            )

            items.append(
                {
                    "title": "Network Activity",
                    "summary": f"↑{self._format_bytes(total_bytes_sent)} ↓{self._format_bytes(total_bytes_recv)}",
                    "link": None,
                    "published": datetime.now().isoformat(),
                    "tags": ["system", "network", "monitoring"],
                    "extra": {
                        "type": "network",
                        "data": data["network"],
                        "alert": False,
                    },
                }
            )

        # Alert summary
        alerts = data.get("alerts", {})
        if alerts:
            items.append(
                {
                    "title": f"System Alerts: {len(alerts)}",
                    "summary": ", ".join(alert["message"] for alert in alerts.values()),
                    "link": None,
                    "published": datetime.now().isoformat(),
                    "tags": ["system", "alerts", "monitoring"],
                    "extra": {
                        "type": "alerts",
                        "data": alerts,
                        "alert": True,
                    },
                }
            )

        return items

    def _format_bytes(self, bytes_value: float) -> str:
        """Format bytes to human readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f}PB"

    def _format_percent(self, value: float) -> str:
        """Format percentage with color coding."""
        return f"{value:.1f}%"

    def _get_status_color(self, percent: float, threshold: float = 80) -> str:
        """Get color based on percentage value."""
        if percent >= threshold:
            return "red"
        elif percent >= threshold * 0.8:
            return "orange"
        else:
            return "green"

    def render(self) -> None:
        """Render the system monitor module UI."""
        data = self.fetch()

        with ui.column().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.GAP_SM}"
        ):
            # Header with refresh button
            with ui.row().classes("w-full justify-between items-center mb-2"):
                ui.label("System Monitor").classes(DashboardStyles.TITLE_H2)
                ui.button("Refresh", on_click=lambda: self.refresh_ui()).props(
                    "dense"
                ).classes("text-xs")

            # System overview cards
            with ui.row().classes("w-full gap-2 flex-wrap"):
                for item in data:
                    if item["extra"]["type"] != "alerts":
                        self._render_metric_card(item)

            # Alerts section
            alerts = [item for item in data if item["extra"]["type"] == "alerts"]
            if alerts:
                self._render_alerts_section(alerts[0])

            # Start auto-refresh
            self._start_monitoring()

    def _render_metric_card(self, item: dict[str, Any]) -> None:
        """Render a metric card."""
        with (
            ui.card().classes(
                f"flex-1 min-w-[120px] {DashboardStyles.PADDING_MD} cursor-pointer hover:shadow-md transition-shadow"
            ),
            ui.column().classes("w-full items-center gap-1"),
        ):
            # Icon
            icon_map = {
                "cpu": "memory",
                "memory": "sd_card",
                "disk": "storage",
                "network": "wifi",
            }
            ui.icon(icon_map.get(item["extra"]["type"], "dashboard")).classes(
                "text-2xl"
            )

            # Title
            ui.label(item["title"]).classes("text-sm font-semibold text-center")

            # Summary
            ui.label(item["summary"]).classes("text-xs text-gray-600 text-center")

            # Alert indicator
            if item["extra"]["alert"]:
                ui.icon("warning").classes("text-red-500 text-sm")

    def _render_alerts_section(self, alert_item: dict[str, Any]) -> None:
        """Render the alerts section."""
        with (
            ui.card().classes("w-full p-3 border-l-4 border-red-500"),
            ui.column().classes("w-full gap-2"),
            ui.row().classes("w-full justify-between items-center"),
        ):
            ui.label("System Alerts").classes("font-semibold text-red-600")
            ui.icon("warning").classes("text-red-500")

        for _alert_key, alert_data in alert_item["extra"]["data"].items():
            with ui.row().classes("w-full gap-2 items-center"):
                ui.icon("error").classes("text-red-500 text-sm")
                ui.label(alert_data["message"]).classes("text-sm flex-1")

    def render_detail(self) -> None:
        """Render detailed system monitoring view."""
        with ui.column().classes("w-full gap-6 max-w-6xl mx-auto"):
            ui.label("System Monitor").classes(
                DashboardStyles.TITLE_H1 + " " + DashboardStyles.TEXT_CENTER
            )

            # System info
            if "system" in self._current_data:
                self._render_system_info()

            # CPU details
            if "cpu" in self._current_data and self._current_data["cpu"]:
                self._render_cpu_details()

            # Memory details
            if "memory" in self._current_data and self._current_data["memory"]:
                self._render_memory_details()

            # Disk details
            if "disk" in self._current_data and self._current_data["disk"]:
                self._render_disk_details()

            # Network details
            if "network" in self._current_data and self._current_data["network"]:
                self._render_network_details()

            # Temperature details
            if (
                "temperature" in self._current_data
                and self._current_data["temperature"]
            ):
                self._render_temperature_details()

            # GPU details
            if "gpu" in self._current_data and self._current_data["gpu"]:
                self._render_gpu_details()

    def _render_system_info(self) -> None:
        """Render system information."""
        system_data = self._current_data["system"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("System Information").classes(DashboardStyles.TITLE_H2 + " mb-3")

            with ui.row().classes("w-full gap-4 flex-wrap"):
                if "system" in system_data:
                    sys_info = system_data["system"]
                    with ui.column().classes("gap-2"):
                        ui.label(
                            f"Platform: {sys_info.get('platform', 'N/A')} {sys_info.get('platform_release', '')}"
                        ).classes(DashboardStyles.BODY_TEXT)
                        ui.label(
                            f"Architecture: {sys_info.get('architecture', 'N/A')}"
                        ).classes(DashboardStyles.BODY_TEXT)
                        ui.label(
                            f"Hostname: {sys_info.get('hostname', 'N/A')}"
                        ).classes(DashboardStyles.BODY_TEXT)
                        ui.label(
                            f"Uptime: {self._format_uptime(sys_info.get('uptime_seconds', 0))}"
                        ).classes(DashboardStyles.BODY_TEXT)

                if "processes" in system_data:
                    proc_info = system_data["processes"]
                    with ui.column().classes("gap-2"):
                        ui.label(
                            f"Processes: {proc_info.get('count', 'N/A')} total, {proc_info.get('running', 'N/A')} running"
                        ).classes(DashboardStyles.BODY_TEXT)

    def _render_cpu_details(self) -> None:
        """Render CPU details."""
        cpu_data = self._current_data["cpu"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("CPU Information").classes(DashboardStyles.TITLE_H2 + " mb-3")

            with ui.row().classes("w-full gap-4 flex-wrap"):
                # CPU usage gauge
                with ui.column().classes("items-center gap-2"):
                    ui.label("CPU Usage").classes(DashboardStyles.TITLE_H2)
                    self._render_gauge(cpu_data.get("percent", 0), 100)

                # CPU details
                with ui.column().classes("gap-2 flex-1"):
                    ui.label(f"Usage: {cpu_data.get('percent', 0):.1f}%").classes(
                        DashboardStyles.BODY_TEXT
                    )
                    ui.label(
                        f"Cores: {cpu_data.get('count', 'N/A')} physical, {cpu_data.get('count_logical', 'N/A')} logical"
                    ).classes(DashboardStyles.BODY_TEXT)

                    if cpu_data.get("frequency"):
                        freq = cpu_data["frequency"]
                        ui.label(
                            f"Frequency: {freq.get('current', 0):.0f} MHz"
                        ).classes(DashboardStyles.BODY_TEXT)

                    if cpu_data.get("load_average"):
                        load = cpu_data["load_average"]
                        ui.label(
                            f"Load Average: {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
                        ).classes(DashboardStyles.BODY_TEXT)

    def _render_memory_details(self) -> None:
        """Render memory details."""
        memory_data = self._current_data["memory"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("Memory Information").classes(DashboardStyles.TITLE_H2 + " mb-3")

            # Virtual memory
            if "virtual" in memory_data:
                vm = memory_data["virtual"]
                with (
                    ui.column().classes("gap-3"),
                    ui.row().classes("w-full gap-4"),
                    ui.column().classes("items-center gap-2"),
                ):
                    ui.label("Virtual Memory").classes(DashboardStyles.TITLE_H2)
                    self._render_gauge(vm.get("percent", 0), 100)
                with ui.column().classes("gap-2 flex-1"):
                    ui.label(
                        f"Total: {self._format_bytes(vm.get('total', 0))}"
                    ).classes(DashboardStyles.BODY_TEXT)
                    ui.label(
                        f"Used: {self._format_bytes(vm.get('used', 0))} ({vm.get('percent', 0):.1f}%)"
                    ).classes(DashboardStyles.BODY_TEXT)
                    ui.label(
                        f"Available: {self._format_bytes(vm.get('available', 0))}"
                    ).classes(DashboardStyles.BODY_TEXT)

            # Swap memory
            if "swap" in memory_data:
                swap = memory_data["swap"]
                if swap.get("total", 0) > 0:
                    with ui.column().classes("gap-3 mt-3"):
                        ui.label("Swap Memory").classes(DashboardStyles.TITLE_H2)
                        with ui.row().classes("w-full gap-4"):
                            with ui.column().classes("items-center gap-2"):
                                self._render_gauge(swap.get("percent", 0), 100)

                            with ui.column().classes("gap-2 flex-1"):
                                ui.label(
                                    f"Total: {self._format_bytes(swap.get('total', 0))}"
                                ).classes(DashboardStyles.BODY_TEXT)
                                ui.label(
                                    f"Used: {self._format_bytes(swap.get('used', 0))} ({swap.get('percent', 0):.1f}%)"
                                ).classes(DashboardStyles.BODY_TEXT)

    def _render_disk_details(self) -> None:
        """Render disk details."""
        disk_data = self._current_data["disk"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("Disk Information").classes(DashboardStyles.TITLE_H2 + " mb-3")

            for path, disk_info in disk_data.items():
                if path == "partitions":
                    continue

                with (
                    ui.column().classes("gap-3 mb-4"),
                    ui.row().classes("w-full gap-4"),
                    ui.column().classes("items-center gap-2"),
                ):
                    ui.label(f"Disk {path}").classes(DashboardStyles.TITLE_H2)
                    if "usage" in disk_info:
                        usage = disk_info["usage"]
                        self._render_gauge(usage.get("percent", 0), 100)

                    if "usage" in disk_info:
                        usage = disk_info["usage"]
                        with ui.column().classes("gap-2 flex-1"):
                            ui.label(
                                f"Total: {self._format_bytes(usage.get('total', 0))}"
                            ).classes(DashboardStyles.BODY_TEXT)
                            ui.label(
                                f"Used: {self._format_bytes(usage.get('used', 0))} ({usage.get('percent', 0):.1f}%)"
                            ).classes(DashboardStyles.BODY_TEXT)
                            ui.label(
                                f"Free: {self._format_bytes(usage.get('free', 0))}"
                            ).classes(DashboardStyles.BODY_TEXT)

    def _render_network_details(self) -> None:
        """Render network details."""
        network_data = self._current_data["network"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("Network Information").classes(DashboardStyles.TITLE_H2 + " mb-3")

            for interface, net_info in network_data.items():
                with ui.column().classes("gap-2 mb-3"):
                    ui.label(f"Interface: {interface}").classes(
                        DashboardStyles.FONT_SEMIBOLD
                    )

                    with ui.row().classes("w-full gap-4 flex-wrap"):
                        with ui.column().classes("gap-1"):
                            ui.label(
                                f"Sent: {self._format_bytes(net_info.get('bytes_sent', 0))}"
                            ).classes(DashboardStyles.BODY_TEXT)
                            ui.label(
                                f"Packets: {net_info.get('packets_sent', 0)}"
                            ).classes(DashboardStyles.BODY_TEXT)

                        with ui.column().classes("gap-1"):
                            ui.label(
                                f"Received: {self._format_bytes(net_info.get('bytes_recv', 0))}"
                            ).classes(DashboardStyles.BODY_TEXT)
                            ui.label(
                                f"Packets: {net_info.get('packets_recv', 0)}"
                            ).classes(DashboardStyles.BODY_TEXT)

                        if net_info.get("addresses", {}).get("ipv4"):
                            ui.label(f"IPv4: {net_info['addresses']['ipv4']}").classes(
                                DashboardStyles.BODY_TEXT
                            )

    def _render_temperature_details(self) -> None:
        """Render temperature details."""
        temp_data = self._current_data["temperature"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("Temperature Information").classes(
                DashboardStyles.TITLE_H2 + " mb-3"
            )

            for sensor, temp_info in temp_data.items():
                with ui.row().classes("w-full gap-4 items-center mb-2"):
                    ui.label(f"{sensor}:").classes(
                        DashboardStyles.FONT_MEDIUM + " flex-1"
                    )

                    current = temp_info.get("current", 0)
                    high = temp_info.get("high")
                    critical = temp_info.get("critical")

                    temp_color = "green"
                    if critical and current >= critical:
                        temp_color = "red"
                    elif high and current >= high:
                        temp_color = "orange"

                    ui.label(f"{current:.1f}°C").classes(
                        DashboardStyles.BODY_TEXT
                        + " "
                        + DashboardStyles.FONT_SEMIBOLD
                        + f" text-{temp_color}"
                    )

                    if high:
                        ui.label(f"(High: {high}°C)").classes(
                            DashboardStyles.SUBTLE_TEXT
                        )

                    if critical:
                        ui.label(f"(Critical: {critical}°C)").classes(
                            DashboardStyles.BODY_TEXT + " text-red-600"
                        )

    def _render_gpu_details(self) -> None:
        """Render GPU details."""
        gpu_data = self._current_data["gpu"]

        with ui.card().classes(
            f"{DashboardStyles.FULL_WIDTH} {DashboardStyles.PADDING_LG}"
        ):
            ui.label("GPU Information").classes(DashboardStyles.TITLE_H2 + " mb-3")

            for gpu_id, gpu_info in gpu_data.items():
                if isinstance(gpu_info, dict) and "name" in gpu_info:
                    with ui.column().classes("gap-3 mb-4"):
                        ui.label(f"{gpu_info['name']} ({gpu_id})").classes(
                            DashboardStyles.TITLE_H2
                        )

                        with ui.row().classes("w-full gap-4 flex-wrap"):
                            # GPU utilization
                            if "utilization" in gpu_info:
                                util = gpu_info["utilization"]
                                with ui.column().classes("items-center gap-2"):
                                    ui.label("GPU Utilization").classes(
                                        DashboardStyles.BODY_TEXT
                                        + " "
                                        + DashboardStyles.FONT_SEMIBOLD
                                    )
                                    self._render_gauge(util.get("gpu", 0), 100)

                            # Memory usage
                            if "memory" in gpu_info:
                                mem = gpu_info["memory"]
                                with ui.column().classes("items-center gap-2"):
                                    ui.label("Memory Usage").classes(
                                        DashboardStyles.BODY_TEXT
                                        + " "
                                        + DashboardStyles.FONT_SEMIBOLD
                                    )
                                    self._render_gauge(mem.get("percent", 0), 100)

                            # Temperature
                            if "temperature" in gpu_info:
                                temp = gpu_info["temperature"]
                                with ui.column().classes("items-center gap-2"):
                                    ui.label("Temperature").classes(
                                        DashboardStyles.BODY_TEXT
                                        + " "
                                        + DashboardStyles.FONT_SEMIBOLD
                                    )
                                    temp_color = "green"
                                    if temp >= 80:
                                        temp_color = "red"
                                    elif temp >= 70:
                                        temp_color = "orange"

                                    ui.label(f"{temp}°C").classes(
                                        DashboardStyles.BODY_TEXT
                                        + " "
                                        + DashboardStyles.FONT_SEMIBOLD
                                        + f" text-{temp_color}"
                                    )

    def _render_gauge(self, value: float, max_value: float) -> None:
        """Render a simple gauge visualization."""
        percent = (value / max_value) * 100 if max_value > 0 else 0

        # Determine color
        if percent >= 90:
            color = "red"
        elif percent >= 70:
            color = "orange"
        else:
            color = "green"

        # Create a simple progress bar
        with (
            ui.card().classes("w-16 h-16 p-1 border-2 border-gray-200"),
            ui.column().classes("w-full h-full justify-center items-center"),
        ):
            ui.label(f"{int(percent)}%").classes(f"text-xs font-bold text-{color}")

    def _format_uptime(self, seconds) -> str:
        """Format uptime in human readable format."""
        seconds = float(seconds)
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def _start_monitoring(self) -> None:
        """Start the background monitoring task."""
        if self._monitoring_task and not self._monitoring_task.done():
            return

        self._monitoring_task = asyncio.create_task(self._monitoring_loop())

    async def _monitoring_loop(self) -> None:
        """Background monitoring loop."""
        while True:
            try:
                await asyncio.sleep(self.config.get("refresh_interval", 2))
                self.refresh_ui()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Monitoring error: {e}")

    def refresh_ui(self) -> None:
        """Refresh the UI with new data."""
        # This would typically trigger a UI refresh
        # For now, we'll just update the internal data
        self._current_data = self.collect_system_data()

    def cleanup(self) -> None:
        """Clean up monitoring resources."""
        if self._monitoring_task and not self._monitoring_task.done():
            self._monitoring_task.cancel()
        super().cleanup()
