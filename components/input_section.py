"""
Task input section – text field, add button, and priority selector.
"""

import customtkinter as ctk


class InputSection(ctk.CTkFrame):
    """Where the user types a new task and chooses its priority."""

    def __init__(self, parent, add_callback, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.add_callback = add_callback
        self.current_priority = "medium"   # default

        self.setup_ui()

    def setup_ui(self):
        """Build the entry, add button and priority radio‑like buttons."""
        # Input row (text field + "Add Task" button)
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 10))

        self.task_input = ctk.CTkEntry(
            input_frame,
            placeholder_text="Add a new task (e.g., 'Complete project report by Friday')",
            font=("Roboto", 14),
            height=50,
            border_width=2,
            border_color="#e9ecef"
        )
        self.task_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

        add_button = ctk.CTkButton(
            input_frame,
            text="Add Task",
            font=("Roboto", 14, "bold"),
            height=50,
            width=120,
            fg_color="#4b6cb7",
            hover_color="#3a5a9a",
            command=self.handle_add_task
        )
        add_button.pack(side="right")

        # Priority row (Low / Medium / High)
        priority_frame = ctk.CTkFrame(self, fg_color="transparent")
        priority_frame.pack(fill="x")

        priority_label = ctk.CTkLabel(
            priority_frame,
            text="Priority:",
            font=("Roboto", 14)
        )
        priority_label.pack(side="left", padx=(0, 10))

        priorities = [
            ("Low", "low", "#2e7d32"),
            ("Medium", "medium", "#4b6cb7"),
            ("High", "high", "#c62828")
        ]

        self.priority_buttons = {}
        for text, value, color in priorities:
            btn = ctk.CTkButton(
                priority_frame,
                text=text,
                font=("Roboto", 12),
                width=80,
                height=30,
                fg_color="#f8f9fa" if value != "medium" else color,
                text_color="black" if value != "medium" else "white",
                hover_color="#e9ecef" if value != "medium" else color,
                border_width=2,
                border_color="#e9ecef" if value != "medium" else color,
                command=lambda v=value, c=color: self.set_priority(v, c)
            )
            btn.pack(side="left", padx=5)
            self.priority_buttons[value] = btn

        # Pressing Enter in the text field also adds the task
        self.task_input.bind("<Return>", lambda e: self.handle_add_task())

    def set_priority(self, priority, color):
        """Change the active priority and update button colours."""
        self.current_priority = priority

        for value, btn in self.priority_buttons.items():
            if value == priority:
                btn.configure(
                    fg_color=color,
                    text_color="white",
                    border_color=color
                )
            else:
                btn.configure(
                    fg_color="#f8f9fa",
                    text_color="black",
                    border_color="#e9ecef"
                )

    def handle_add_task(self):
        """Take the text from the entry, call the add callback, then clear the field."""
        text = self.task_input.get()
        if text.strip():
            self.add_callback(text, self.current_priority)
            self.task_input.delete(0, "end")
            self.task_input.focus()