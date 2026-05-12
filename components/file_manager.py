"""
File management section – a card with buttons for exporting, importing,
previewing JSON and clearing all tasks.
"""

import customtkinter as ctk


class FileManager(ctk.CTkFrame):
    """UI frame that holds the data management controls."""

    def __init__(self, parent, export_callback, import_callback,
                 preview_callback, clear_callback, **kwargs):
        super().__init__(
            parent,
            fg_color="#f8f9ff",
            corner_radius=15,
            border_width=2,
            border_color="#6c5ce7",
            **kwargs
        )

        # Store callbacks that will be triggered by the buttons
        self.export_callback = export_callback
        self.import_callback = import_callback
        self.preview_callback = preview_callback
        self.clear_callback = clear_callback

        self.setup_ui()

    def setup_ui(self):
        """Create the labels and buttons."""
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Task Data Management",
            font=("Poppins", 18, "bold"),
            text_color="#182848"
        )
        title_label.pack(anchor="w", padx=20, pady=(20, 10))

        # Description
        desc_label = ctk.CTkLabel(
            self,
            text="Your tasks are stored in a local JSON file format. You can export, import, or manage your tasks.",
            font=("Roboto", 14),
            text_color="#6c757d",
            wraplength=800,
            justify="left"
        )
        desc_label.pack(fill="x", padx=20, pady=(0, 10))

        # Inform the user about the default file name
        file_info = ctk.CTkLabel(
            self,
            text="Current File: tasks.json",
            font=("Roboto", 12),
            text_color="#4b6cb7"
        )
        file_info.pack(anchor="w", padx=20, pady=(0, 20))

        # Buttons row
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))

        export_btn = ctk.CTkButton(
            buttons_frame,
            text="Export to JSON",
            font=("Roboto", 14, "bold"),
            height=40,
            fg_color="#e8f5e9",
            text_color="#2e7d32",
            hover_color="#2e7d32",
            border_width=2,
            border_color="#c8e6c9",
            command=self.export_callback
        )
        export_btn.pack(side="left", padx=5)

        import_btn = ctk.CTkButton(
            buttons_frame,
            text="Import from JSON",
            font=("Roboto", 14, "bold"),
            height=40,
            fg_color="#e3f2fd",
            text_color="#1565c0",
            hover_color="#1565c0",
            border_width=2,
            border_color="#bbdefb",
            command=self.import_callback
        )
        import_btn.pack(side="left", padx=5)

        preview_btn = ctk.CTkButton(
            buttons_frame,
            text="View JSON Data",
            font=("Roboto", 14, "bold"),
            height=40,
            fg_color="#f8f9fa",
            text_color="#4b6cb7",
            hover_color="#4b6cb7",
            border_width=2,
            border_color="#e9ecef",
            command=self.preview_callback
        )
        preview_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear All Tasks",
            font=("Roboto", 14, "bold"),
            height=40,
            fg_color="#ffebee",
            text_color="#c62828",
            hover_color="#c62828",
            border_width=2,
            border_color="#ffcdd2",
            command=self.clear_callback
        )
        clear_btn.pack(side="left", padx=5)