"""
Footer section – contains copyright notice and links to Help / About.
"""

import customtkinter as ctk


class FooterSection(ctk.CTkFrame):
    """Simple footer at the bottom of the main content area."""

    def __init__(self, parent, help_callback, about_callback, **kwargs):
        super().__init__(
            parent,
            fg_color="#f9fafc",
            corner_radius=10,
            **kwargs
        )

        self.help_callback = help_callback
        self.about_callback = about_callback

        self.setup_ui()

    def setup_ui(self):
        """Place the copyright text and interactive links."""
        copyright_label = ctk.CTkLabel(
            self,
            text="To Do List App © 2025 | Your Personal Task Management Solution",
            font=("Roboto", 12),
            text_color="#6c757d"
        )
        copyright_label.pack(pady=(15, 10))

        links_frame = ctk.CTkFrame(self, fg_color="transparent")
        links_frame.pack(pady=(0, 10))

        help_btn = ctk.CTkButton(
            links_frame,
            text="Help & Guide",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#4b6cb7",
            hover_color="#f8f9fa",
            command=self.help_callback
        )
        help_btn.pack(side="left", padx=20)

        about_btn = ctk.CTkButton(
            links_frame,
            text="About",
            font=("Roboto", 12),
            fg_color="transparent",
            text_color="#4b6cb7",
            hover_color="#f8f9fa",
            command=self.about_callback
        )
        about_btn.pack(side="left", padx=20)