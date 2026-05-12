"""
Header section – displays the application title and a short tagline.
"""

import customtkinter as ctk


class HeaderSection(ctk.CTkFrame):
    """Top part of the app with the logo text and a decorative line."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.setup_ui()

    def setup_ui(self):
        """Create the title, subtitle and a separator line."""
        title_label = ctk.CTkLabel(
            self,
            text="📝 To Do List",
            font=("Poppins", 42, "bold"),
            text_color="#182848"
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Organize your tasks, boost your productivity",
            font=("Roboto", 14),
            text_color="#6c757d"
        )
        subtitle_label.pack()

        # A thin line to visually separate the header from the rest
        line = ctk.CTkFrame(self, height=2, fg_color="#e9ecef")
        line.pack(fill="x", pady=(10, 0))