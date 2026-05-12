"""
Main application window for the To-Do List app.

This module ties together all UI components (header, stats, input, task list,
file manager, footer) and handles the core logic: adding, editing, deleting,
filtering, saving/loading tasks, and showing notifications/modals.
"""

import customtkinter as ctk
from datetime import datetime
import json
import os
from typing import List, Dict, Optional

# Import our custom components
from components.header import HeaderSection
from components.stats import StatsSection
from components.input_section import InputSection
from components.task_list import TaskList
from components.file_manager import FileManager
from components.footer import FooterSection
from components.modals import HelpModal, AboutModal, JsonPreviewModal
from models.task import Task


class TodoApp:
    """Main application window – ties everything together."""

    def __init__(self):
        # Set up the root window
        self.window = ctk.CTk()
        self.window.title("To Do List")
        self.window.geometry("1000x800")
        self.window.minsize(800, 600)

        # Application data
        self.tasks: List[Task] = []                # all tasks
        self.current_filter = "all"               # all / pending / completed / high
        self.stats_data = {
            "total": 0,
            "completed": 0,
            "pending": 0,
            "high_priority": 0
        }

        # Where tasks are stored (local JSON file)
        self.data_file = "tasks.json"

        # Build the UI
        self.setup_ui()
        self.load_tasks()      # load existing tasks from disk

        # Keep references to modals so we reuse them
        self.modals = {}

    def setup_ui(self):
        """Create and arrange all UI components inside the main window."""
        # Main container with padding
        self.container = ctk.CTkFrame(self.window)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Make the whole content scrollable (important for many tasks)
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.container,
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True)

        # 1) Header (title & subtitle)
        self.header = HeaderSection(self.scroll_frame)
        self.header.pack(fill="x", pady=(0, 10))

        # 2) Statistics (total, completed, pending, high priority)
        self.stats = StatsSection(self.scroll_frame, self.stats_data)
        self.stats.pack(fill="x", pady=(0, 10))

        # 3) Main content area (white card)
        self.content_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="white",
            corner_radius=15
        )
        self.content_frame.pack(fill="both", expand=True)

        # 4) Input section (text field + priority buttons)
        self.input_section = InputSection(
            self.content_frame,
            self.add_task
        )
        self.input_section.pack(fill="x", padx=20, pady=20)

        # 5) Filter buttons (All / Pending / Completed / High)
        self.create_filter_buttons()

        # 6) Scrollable task list (shows tasks according to current filter)
        self.task_list = TaskList(
            self.content_frame,
            self.tasks,
            self.toggle_task,
            self.edit_task,
            self.delete_task
        )
        self.task_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 7) Empty state label – shown when no tasks match the filter
        self.empty_state_label = ctk.CTkLabel(
            self.content_frame,
            text="No tasks to display\nAdd your first task using the input field above",
            font=("Roboto", 16),
            text_color="#6c757d",
            justify="center"
        )

        # 8) File management section (export, import, preview, clear)
        self.file_manager = FileManager(
            self.content_frame,
            self.export_tasks,
            self.import_tasks,
            self.show_json_preview,
            self.clear_all_tasks
        )
        self.file_manager.pack(fill="x", padx=20, pady=(0, 20))

        # 9) Footer (Help, About links)
        self.footer = FooterSection(
            self.content_frame,
            self.show_help,
            self.show_about
        )
        self.footer.pack(fill="x", padx=20, pady=(0, 10))

    def create_filter_buttons(self):
        """Create the four filter buttons (All, Pending, Completed, High)."""
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=(0, 10))

        filters = [
            ("All Tasks", "all", "layer-group"),
            ("Pending", "pending", "clock"),
            ("Completed", "completed", "check-circle"),
            ("High Priority", "high", "exclamation-circle")
        ]

        for text, filter_type, icon in filters:
            # The "All" button starts as active (blue), others white
            btn = ctk.CTkButton(
                filter_frame,
                text=f" {text}",
                font=("Roboto", 14, "bold"),
                corner_radius=20,
                border_width=2,
                border_color="#e9ecef",
                fg_color="white" if filter_type != "all" else "#4b6cb7",
                text_color="black" if filter_type != "all" else "white",
                hover_color="#f8f9fa" if filter_type != "all" else "#3a5a9a",
                command=lambda ft=filter_type: self.apply_filter(ft)
            )
            btn.pack(side="left", padx=5)

    # ---------- Task management ----------
    def add_task(self, text: str, priority: str):
        """Create a new task and add it to the list."""
        if not text.strip():
            self.show_notification("Please enter a task!", "warning")
            return

        task = Task(
            text=text.strip(),
            priority=priority,
            created_at=datetime.now()
        )
        self.tasks.append(task)
        self.save_tasks()

        # Switch filter to "all" so the new task is immediately visible
        self.current_filter = "all"
        self.update_ui()
        self.show_notification("Task added successfully!", "success")

    def toggle_task(self, task_id: str):
        """Mark a task as completed / not completed."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                break
        self.save_tasks()
        self.update_ui()

    def edit_task(self, task_id: str):
        """Show a dialog to edit the task's text."""
        # Locate the task
        task_to_edit = next((task for task in self.tasks if task.id == task_id), None)
        if not task_to_edit:
            return

        # Simple input dialog
        dialog = ctk.CTkInputDialog(
            text=f"Edit task (current: {task_to_edit.text}):",
            title="Edit Task"
        )
        new_text = dialog.get_input()
        if new_text and new_text.strip():
            task_to_edit.text = new_text.strip()
            self.save_tasks()
            self.update_ui()
            self.show_notification("Task updated!", "success")

    def delete_task(self, task_id: str):
        """Remove a task after confirmation."""
        from tkinter import messagebox
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this task?"
        )
        if confirm:
            self.tasks = [task for task in self.tasks if task.id != task_id]
            self.save_tasks()
            self.update_ui()
            self.show_notification("Task deleted!", "info")

    # ---------- Filtering ----------
    def apply_filter(self, filter_type: str):
        """Change the current filter and refresh the UI."""
        self.current_filter = filter_type
        self.update_ui()

    def get_filtered_tasks(self):
        """Return the tasks that match the current filter."""
        if self.current_filter == "all":
            return self.tasks
        elif self.current_filter == "pending":
            return [task for task in self.tasks if not task.completed]
        elif self.current_filter == "completed":
            return [task for task in self.tasks if task.completed]
        elif self.current_filter == "high":
            return [task for task in self.tasks if task.priority == "high"]
        return self.tasks

    # ---------- Stats & UI refresh ----------
    def update_stats(self):
        """Recalculate the statistics from the current tasks."""
        self.stats_data["total"] = len(self.tasks)
        self.stats_data["completed"] = len([t for t in self.tasks if t.completed])
        self.stats_data["pending"] = self.stats_data["total"] - self.stats_data["completed"]
        self.stats_data["high_priority"] = len([t for t in self.tasks if t.priority == "high"])

        if hasattr(self, 'stats'):
            self.stats.update_stats(self.stats_data)

    def update_ui(self):
        """Refresh the whole interface: stats, empty state, task list."""
        self.update_stats()

        filtered = self.get_filtered_tasks()
        if not filtered:
            self.empty_state_label.pack(pady=50)
        else:
            self.empty_state_label.pack_forget()

        self.task_list.update_tasks(filtered)

    # ---------- Persistence (JSON) ----------
    def load_tasks(self):
        """Load tasks from tasks.json (supports both old list format and new dict format)."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)

                if isinstance(data, list):
                    # Legacy format: just an array of tasks
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                elif isinstance(data, dict) and "tasks" in data:
                    # New format with metadata
                    self.tasks = [Task.from_dict(task_data) for task_data in data["tasks"]]
                else:
                    self.tasks = []

                self.update_ui()
                self.show_notification(f"Loaded {len(self.tasks)} tasks", "success")
            else:
                self.tasks = []
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
            self.show_notification("Error loading tasks – starting fresh", "error")

    def save_tasks(self):
        """Write current tasks to tasks.json (simple list format)."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2, default=str)
        except Exception as e:
            self.show_notification(f"Save failed: {e}", "error")

    # ---------- File management (export / import) ----------
    def export_tasks(self):
        """Export tasks to a user‑chosen JSON file (with metadata)."""
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    data = {
                        "version": "1.0",
                        "generated_at": datetime.now().isoformat(),
                        "total_tasks": len(self.tasks),
                        "completed_tasks": len([t for t in self.tasks if t.completed]),
                        "tasks": [task.to_dict() for task in self.tasks]
                    }
                    json.dump(data, f, indent=2, default=str)
                self.show_notification(f"Tasks exported to {file_path}", "success")
            except Exception as e:
                self.show_notification(f"Error exporting tasks: {e}", "error")

    def import_tasks(self):
        """Import tasks from a JSON file (replace or merge)."""
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                imported_tasks = []
                if isinstance(data, list):
                    imported_tasks = [Task.from_dict(task_data) for task_data in data]
                elif isinstance(data, dict) and "tasks" in data:
                    imported_tasks = [Task.from_dict(task_data) for task_data in data["tasks"]]

                action = messagebox.askyesno(
                    "Import Tasks",
                    f"Found {len(imported_tasks)} tasks. Replace current tasks? (No to merge)"
                )
                if action:
                    self.tasks = imported_tasks
                else:
                    existing_ids = {task.id for task in self.tasks}
                    for task in imported_tasks:
                        if task.id not in existing_ids:
                            self.tasks.append(task)

                self.save_tasks()
                self.update_ui()
                self.show_notification(f"Imported {len(imported_tasks)} tasks", "success")
            except Exception as e:
                self.show_notification(f"Error importing tasks: {e}", "error")

    def clear_all_tasks(self):
        """Delete all tasks after confirmation."""
        from tkinter import messagebox
        confirm = messagebox.askyesno(
            "Clear All Tasks",
            "Are you sure you want to delete ALL tasks? This cannot be undone."
        )
        if confirm:
            self.tasks = []
            self.save_tasks()
            self.update_ui()
            self.show_notification("All tasks cleared!", "info")

    def show_json_preview(self):
        """Show a modal with a pretty JSON representation of the current tasks."""
        if not self.tasks:
            self.show_notification("No tasks to preview!", "warning")
            return

        data = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t.completed]),
            "tasks": [task.to_dict() for task in self.tasks]
        }

        if "json_preview" not in self.modals:
            self.modals["json_preview"] = JsonPreviewModal(self.window)
        self.modals["json_preview"].show(data)

    # ---------- Help and About ----------
    def show_help(self):
        """Display the help modal with tabs (Getting started, Features, etc.)."""
        if "help" not in self.modals:
            self.modals["help"] = HelpModal(self.window)
        self.modals["help"].show()

    def show_about(self):
        """Display the about modal with version and tech info."""
        if "about" not in self.modals:
            self.modals["about"] = AboutModal(self.window)
        self.modals["about"].show()

    # ---------- Notifications ----------
    def show_notification(self, message: str, type: str = "info"):
        """Popup a temporary message near the top of the window."""
        colors = {
            "success": "#28a745",
            "warning": "#ffc107",
            "error": "#dc3545",
            "info": "#4b6cb7"
        }
        notification = ctk.CTkLabel(
            self.window,
            text=message,
            font=("Roboto", 14),
            text_color="white",
            fg_color=colors.get(type, "#4b6cb7"),
            corner_radius=10,
            height=40
        )
        notification.place(relx=0.5, y=50, anchor="center")
        self.window.after(3000, notification.destroy)

    def run(self):
        """Start the main event loop."""
        self.window.mainloop()