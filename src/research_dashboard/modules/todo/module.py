"""Todo module for managing tasks and to-do items."""

from datetime import datetime
from typing import Any

from nicegui import ui

from ..extended import ExtendedModule


class TodoModule(ExtendedModule):
    """Todo module for managing tasks and to-do items."""

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.todos = self._load_todos()
        self.todo_input = None
        self.todos_list = None
    
    def has_persistence(self) -> bool:
        """Todo module requires persistent storage."""
        return True

    @property
    def id(self) -> str:
        return "todo"

    @property
    def name(self) -> str:
        return "Todo"

    @property
    def icon(self) -> str:
        return "checklist"

    @property
    def description(self) -> str:
        return "Manage your tasks and to-do items"

    @property
    def version(self) -> str:
        return "1.0.0"

    def _load_todos(self) -> list[dict[str, Any]]:
        """Load todos from storage or return default todos."""
        storage = self.get_storage()
        todos = storage.get("todos")
        
        if todos:
            return todos

        # Default todos
        return [
            {"id": 1, "text": "Welcome to Research Dashboard!", "completed": False, "created": datetime.now().isoformat()},
            {"id": 2, "text": "Add your own tasks here", "completed": False, "created": datetime.now().isoformat()},
            {"id": 3, "text": "Check the weather module", "completed": True, "created": datetime.now().isoformat()}
        ]

    def _save_todos(self) -> None:
        """Save todos to storage."""
        storage = self.get_storage()
        storage.set("todos", self.todos)

    def _add_todo(self, text: str) -> None:
        """Add a new todo item."""
        if text.strip():
            new_todo = {
                "id": max([t.get("id", 0) for t in self.todos]) + 1 if self.todos else 1,
                "text": text.strip(),
                "completed": False,
                "created": datetime.now().isoformat()
            }
            self.todos.insert(0, new_todo)
            self._save_todos()
            self._refresh_todo_list()
            if self.todo_input:
                self.todo_input.value = ""

    def _toggle_todo(self, todo_id: int) -> None:
        """Toggle todo completion status."""
        for todo in self.todos:
            if todo.get("id") == todo_id:
                todo["completed"] = not todo["completed"]
                self._save_todos()
                self._refresh_todo_list()
                break

    def _delete_todo(self, todo_id: int) -> None:
        """Delete a todo item."""
        self.todos = [t for t in self.todos if t.get("id") != todo_id]
        self._save_todos()
        self._refresh_todo_list()

    def _refresh_todo_list(self) -> None:
        """Refresh the todo list display."""
        if self.todos_list:
            self.todos_list.clear()
            with self.todos_list:
                self._render_todo_items()

    def _render_todo_items(self) -> None:
        """Render the todo items."""
        if not self.todos:
            ui.label("No tasks yet. Add one above!").classes("text-gray-500 text-center w-full")
            return

        for todo in self.todos:
            with ui.row().classes("w-full items-center gap-2 p-2 rounded-lg hover:bg-gray-50"):
                # Checkbox
                ui.checkbox(
                    value=todo.get("completed", False),
                    on_change=lambda _, tid=todo.get("id"): self._toggle_todo(tid)
                ).classes("text-blue-600")

                # Todo text
                text_class = "line-through text-gray-500" if todo.get("completed") else "text-gray-800"
                ui.label(todo.get("text", "")).classes(f"flex-1 {text_class}")

                # Delete button
                ui.button(
                    icon="delete",
                    on_click=lambda _, tid=todo.get("id"): self._delete_todo(tid)
                ).classes(
                    "text-red-500 hover:text-red-700 hover:bg-red-50 "
                    "transition-colors duration-200"
                ).props("flat dense")

    def fetch(self) -> list[dict[str, Any]]:
        """Fetch todo items."""
        completed_count = sum(1 for todo in self.todos if todo.get("completed"))
        return [{
            "title": f"Todo List ({completed_count}/{len(self.todos)} completed)",
            "summary": "Manage your tasks and to-do items",
            "link": "",
            "published": datetime.now().isoformat(),
            "tags": ["todo", "tasks"],
            "extra": {
                "total": len(self.todos),
                "completed": completed_count,
                "pending": len(self.todos) - completed_count
            }
        }]

    def render(self) -> None:
        """Render the todo module UI."""
        with ui.column().classes("w-full gap-3"):
            # Add todo input
            with ui.row().classes("w-full gap-2"):
                self.todo_input = ui.input(
                    placeholder="Add a new task...",
                    on_change=lambda e: None
                ).classes("flex-1")

                ui.button(
                    icon="add",
                    on_click=lambda: self._add_todo(self.todo_input.value or "")
                ).classes(
                    "bg-blue-500 text-white hover:bg-blue-600 "
                    "transition-colors duration-200"
                ).props("round")

            # Todo list
            self.todos_list = ui.column().classes("w-full gap-1")
            with self.todos_list:
                self._render_todo_items()

    def render_detail(self) -> None:
        """Render detailed todo view."""
        with ui.column().classes("w-full gap-6 max-w-2xl mx-auto"):
            ui.label("Task Manager").classes("text-3xl font-bold text-center")

            # Stats
            completed_count = sum(1 for todo in self.todos if todo.get("completed"))
            with ui.row().classes("w-full justify-center gap-6"):
                with ui.card().classes("p-4 text-center"):
                    ui.label(str(len(self.todos))).classes("text-2xl font-bold text-blue-600")
                    ui.label("Total Tasks").classes("text-sm text-gray-600")

                with ui.card().classes("p-4 text-center"):
                    ui.label(str(completed_count)).classes("text-2xl font-bold text-green-600")
                    ui.label("Completed").classes("text-sm text-gray-600")

                with ui.card().classes("p-4 text-center"):
                    ui.label(str(len(self.todos) - completed_count)).classes("text-2xl font-bold text-orange-600")
                    ui.label("Pending").classes("text-sm text-gray-600")

            # Add todo section
            with ui.card().classes("w-full p-4"):
                ui.label("Add New Task").classes("text-lg font-semibold mb-3")
                with ui.row().classes("w-full gap-2"):
                    self.todo_input = ui.input(
                        placeholder="What needs to be done?",
                        on_change=lambda e: None
                    ).classes("flex-1")

                    ui.button(
                        icon="add",
                        on_click=lambda: self._add_todo(self.todo_input.value or "")
                    ).classes(
                        "bg-blue-500 text-white hover:bg-blue-600 "
                        "transition-colors duration-200"
                    ).props("round")

            # Todo list section
            with ui.card().classes("w-full p-4"):
                ui.label("All Tasks").classes("text-lg font-semibold mb-3")
                self.todos_list = ui.column().classes("w-full gap-2")
                with self.todos_list:
                    self._render_todo_items()
