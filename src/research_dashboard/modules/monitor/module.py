"""Monitor module for checking website availability and response times."""

import time
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from nicegui import ui

from ..extended import ExtendedModule


class MonitorModule(ExtendedModule):
    """Monitor module for checking website availability and response times."""

    @property
    def id(self) -> str:
        return "monitor"

    @property
    def name(self) -> str:
        return "Site Monitor"

    @property
    def icon(self) -> str:
        return "monitor_heart"

    @property
    def description(self) -> str:
        return "Monitor website availability and response times"

    @property
    def version(self) -> str:
        return "1.0.0"

    def _check_site(self, url: str, timeout: int = 10) -> dict[str, Any]:
        """Check if a website is accessible and measure response time."""
        result = {
            "url": url,
            "status": "unknown",
            "response_time": 0,
            "status_code": None,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            result["url"] = url

        try:
            start_time = time.time()
            
            # Create request with user agent to avoid blocking
            request = Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urlopen(request, timeout=timeout) as response:
                response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                result.update({
                    "status": "online",
                    "response_time": round(response_time, 2),
                    "status_code": response.getcode(),
                    "error": None
                })
                
        except HTTPError as e:
            response_time = (time.time() - start_time) * 1000
            result.update({
                "status": "error",
                "response_time": round(response_time, 2),
                "status_code": e.code,
                "error": f"HTTP {e.code}: {e.reason}"
            })
            
        except URLError as e:
            response_time = (time.time() - start_time) * 1000
            result.update({
                "status": "offline",
                "response_time": round(response_time, 2),
                "status_code": None,
                "error": str(e.reason)
            })
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            result.update({
                "status": "error",
                "response_time": round(response_time, 2),
                "status_code": None,
                "error": str(e)
            })

        return result

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch monitoring status for all configured sites."""
        sites = self.config.get("sites", [
            "https://www.google.com",
            "https://www.github.com",
            "https://www.baidu.com",
            "https://api.github.com"
        ])
        
        timeout = self.config.get("timeout", 10)
        results = []
        
        for site in sites:
            result = self._check_site(site, timeout)
            results.append({
                "title": f"{result['url']} - {result['status'].upper()}",
                "summary": f"Response: {result['response_time']}ms | Status: {result['status_code'] or 'N/A'}",
                "link": result["url"],
                "published": result["timestamp"],
                "tags": ["monitor", result["status"], "website"],
                "extra": result
            })
        
        return results

    def render(self) -> None:
        """Render the monitor module UI."""
        data = self.fetch()
        
        with ui.column().classes("w-full gap-2"):
            if not data:
                ui.label("No sites configured").classes("text-gray-500")
                return

            # Show monitoring summary
            online_count = sum(1 for item in data if item["extra"]["status"] == "online")
            total_count = len(data)
            
            with ui.row().classes("w-full justify-between items-center mb-2"):
                ui.label("Site Monitor").classes("text-lg font-semibold")
                ui.label(f"{online_count}/{total_count} online").classes(
                    f"text-sm {'text-green-600' if online_count == total_count else 'text-orange-600'}"
                )

            # Show sites status
            for item in data[:5]:  # Show first 5 sites
                extra = item["extra"]
                status = extra["status"]
                
                status_colors = {
                    "online": "text-green-600",
                    "offline": "text-red-600", 
                    "error": "text-orange-600",
                    "unknown": "text-gray-600"
                }
                
                status_icons = {
                    "online": "check_circle",
                    "offline": "error",
                    "error": "warning",
                    "unknown": "help"
                }

                with ui.card().classes("w-full p-3 cursor-pointer hover:shadow-md transition-shadow"):
                    with ui.row().classes("w-full justify-between items-center"):
                        # Site info
                        with ui.column().classes("gap-1 flex-1"):
                            ui.label(extra["url"]).classes("text-sm font-medium truncate")
                            
                            # Status and response time
                            with ui.row().classes("gap-2 items-center"):
                                ui.icon(status_icons.get(status, "help")).classes(
                                    f"text-{status_colors.get(status, 'gray')} text-sm"
                                )
                                ui.label(status.upper()).classes(
                                    f"text-xs font-semibold {status_colors.get(status, 'text-gray-600')}"
                                )
                                
                                if extra["response_time"] > 0:
                                    time_color = "text-green-600" if extra["response_time"] < 1000 else "text-orange-600"
                                    ui.label(f"{extra['response_time']}ms").classes(f"text-xs {time_color}")
                                
                                if extra.get("status_code"):
                                    ui.label(f"HTTP {extra['status_code']}").classes("text-xs text-gray-500")

                        # Error indicator
                        if extra.get("error") and status != "online":
                            ui.icon("error").classes("text-red-500 text-sm")

    def render_detail(self) -> None:
        """Render detailed monitoring view."""
        data = self.fetch()
        
        with ui.column().classes("w-full gap-6 max-w-4xl mx-auto"):
            ui.label("Site Monitor").classes("text-3xl font-bold text-center")
            
            # Summary statistics
            online_count = sum(1 for item in data if item["extra"]["status"] == "online")
            offline_count = sum(1 for item in data if item["extra"]["status"] == "offline")
            error_count = sum(1 for item in data if item["extra"]["status"] == "error")
            total_count = len(data)
            
            with ui.row().classes("w-full justify-center gap-4 mb-6"):
                with ui.card().classes("p-4 text-center"):
                    ui.label(str(total_count)).classes("text-2xl font-bold text-blue-600")
                    ui.label("Total Sites").classes("text-sm text-gray-600")
                
                with ui.card().classes("p-4 text-center"):
                    ui.label(str(online_count)).classes("text-2xl font-bold text-green-600")
                    ui.label("Online").classes("text-sm text-gray-600")
                
                with ui.card().classes("p-4 text-center"):
                    ui.label(str(offline_count)).classes("text-2xl font-bold text-red-600")
                    ui.label("Offline").classes("text-sm text-gray-600")
                
                with ui.card().classes("p-4 text-center"):
                    ui.label(str(error_count)).classes("text-2xl font-bold text-orange-600")
                    ui.label("Errors").classes("text-sm text-gray-600")
            
            # Sites list
            ui.label("Monitoring Results").classes("text-xl font-semibold")
            
            with ui.column().classes("w-full gap-3"):
                for item in data:
                    extra = item["extra"]
                    status = extra["status"]
                    
                    status_colors = {
                        "online": "green",
                        "offline": "red", 
                        "error": "orange",
                        "unknown": "gray"
                    }
                    
                    status_icons = {
                        "online": "check_circle",
                        "offline": "error",
                        "error": "warning",
                        "unknown": "help"
                    }
                    
                    with ui.card().classes(f"w-full p-4 border-l-4 border-{status_colors.get(status, 'gray')}"):
                        with ui.column().classes("w-full gap-3"):
                            # Header
                            with ui.row().classes("w-full justify-between items-start"):
                                with ui.column().classes("gap-1"):
                                    ui.label(extra["url"]).classes("text-lg font-semibold")
                                    
                                    with ui.row().classes("gap-2 items-center"):
                                        ui.icon(status_icons.get(status, "help")).classes(
                                            f"text-{status_colors.get(status, 'gray')}"
                                        )
                                        ui.label(status.upper()).classes(
                                            f"text-sm font-bold text-{status_colors.get(status, 'gray')}"
                                        )
                                        
                                        if extra["response_time"] > 0:
                                            time_color = "green" if extra["response_time"] < 1000 else "orange"
                                            ui.label(f"{extra['response_time']}ms").classes(f"text-sm text-{time_color}")
                                        
                                        if extra.get("status_code"):
                                            ui.label(f"HTTP {extra['status_code']}").classes("text-sm text-gray-500")
                                
                                # Action buttons
                                with ui.row().classes("gap-2"):
                                    ui.button(
                                        "Open",
                                        on_click=lambda url=extra["url"]: ui.navigate.to(url)
                                    ).classes(
                                        "text-xs bg-blue-500 text-white hover:bg-blue-600"
                                    ).props("target=_blank dense")
                                    
                                    ui.button(
                                        "Refresh",
                                        on_click=lambda: None  # TODO: Implement refresh
                                    ).classes(
                                        "text-xs bg-gray-500 text-white hover:bg-gray-600"
                                    ).props("dense")
                            
                            # Error details
                            if extra.get("error") and status != "online":
                                with ui.expansion("Error Details").classes("w-full"):
                                    ui.label(extra["error"]).classes("text-sm text-red-600")
                            
                            # Timestamp
                            with ui.row().classes("w-full justify-end"):
                                ui.label(f"Checked: {datetime.fromisoformat(extra['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}").classes(
                                    "text-xs text-gray-500"
                                )