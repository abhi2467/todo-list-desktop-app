"""
Task list component – a scrollable container that shows one widget per task.
Each task shows a checkbox, text, priority badge, creation date, edit and delete buttons.
"""

import customtkinter as ctk
from datetime import datetime


class TaskList(ctk.CTkScrollableFrame):
    """Dynamic list of task widgets that updates when the task collection changes."""

    def __init__(self, parent, tasks, toggle_callback, edit_callback, delete_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.tasks = tasks
        self.toggle_callback = toggle_callback
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback

        self.task_widgets = {}   # map task.id -> frame

    def update_tasks(self, tasks):
        """Replace the displayed list with a new set of tasks."""
        self.tasks = tasks

        # Remove all existing child widgets
        for widget in self.winfo_children():
            widget.destroy()
        self.task_widgets.clear()

        # Create a new widget for each task
        for task in tasks:
            self.add_task_widget(task)

    def add_task_widget(self, task):
        """Build a single task row (frame with all controls)."""
        # Border colour depends on priority
        border_colors = {
            "low": "#2e7d32",
            "medium": "#4b6cb7",
            "high": "#c62828"
        }
        # Slight background change for completed tasks
        bg_color = "#f8fff9" if task.completed else "white"

        task_frame = ctk.CTkFrame(
            self,
            fg_color=bg_color,
            corner_radius=10,
            border_width=2,
            border_color=border_colors.get(task.priority, "#4b6cb7")
        )
        task_frame.pack(fill="x", pady=5)

        content = ctk.CTkFrame(task_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Left side: checkbox + task text
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        checkbox = ctk.CTkCheckBox(
            left,
            text="",
            width=24,
            height=24,
            command=lambda t=task: self.toggle_callback(t.id)
        )
        if task.completed:
            checkbox.select()
        else:
            checkbox.deselect()
        checkbox.pack(side="left", padx=(0, 10))

        task_text = ctk.CTkLabel(
            left,
            text=task.text,
            font=("Roboto", 14),
            text_color="#343a40" if not task.completed else "#6c757d",
            justify="left",
            wraplength=500
        )
        task_text.pack(side="left", fill="x", expand=True)

        # Right side: priority badge, date, action buttons
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right")

        # Priority badge (coloured pill)
        priority_colors = {
            "low": ("#2e7d32", "#e8f5e9"),
            "medium": ("#ef6c00", "#fff3e0"),
            "high": ("#c62828", "#ffebee")
        }
        txt_color, bg = priority_colors.get(task.priority, ("#6c757d", "#f8f9fa"))
        badge = ctk.CTkFrame(right, fg_color=bg, corner_radius=15)
        badge.pack(side="left", padx=5)
        ctk.CTkLabel(badge, text=f"{task.priority} priority", font=("Roboto", 10),
                     text_color=txt_color).pack(padx=10, pady=3)

        # Creation date (short format)
        date_str = task.created_at.strftime("%b %d")
        if task.created_at.year != datetime.now().year:
            date_str += f", {task.created_at.year}"
        date_label = ctk.CTkLabel(right, text=f"Added: {date_str}",
                                  font=("Roboto", 11), text_color="#6c757d")
        date_label.pack(side="left", padx=10)

        # Edit and delete buttons
        actions = ctk.CTkFrame(right, fg_color="transparent")
        actions.pack(side="left", padx=(10, 0))

        edit_btn = ctk.CTkButton(
            actions, text="✏️", width=35, height=35, font=("Roboto", 14),
            fg_color="transparent", hover_color="#fff3e0", text_color="#ffc107",
            command=lambda t=task: self.edit_callback(t.id)
        )
        edit_btn.pack(side="left", padx=2)

        delete_btn = ctk.CTkButton(
            actions, text="🗑️", width=35, height=35, font=("Roboto", 14),
            fg_color="transparent", hover_color="#ffebee", text_color="#dc3545",
            command=lambda t=task: self.delete_callback(t.id)
        )
        delete_btn.pack(side="left", padx=2)

        self.task_widgets[task.id] = task_frame