"""
Statistics section – displays four cards with total, completed, pending and high‑priority tasks.
"""

import customtkinter as ctk


class StatsSection(ctk.CTkFrame):
    """A grid of four statistic cards that update automatically."""

    def __init__(self, parent, stats_data, **kwargs):
        super().__init__(parent, fg_color="#f0f4ff", **kwargs)

        self.stats_data = stats_data
        self.stats_labels = {}       # to store the value label widgets

        self.setup_ui()

    def setup_ui(self):
        """Create the four cards in a grid."""
        # Make columns equally sized
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        stats_info = [
            ("Total Tasks", "list-check", "#4b6cb7"),
            ("Completed", "check-circle", "#28a745"),
            ("Pending", "clock", "#ffc107"),
            ("High Priority", "star", "#dc3545")
        ]

        for i, (label, icon, color) in enumerate(stats_info):
            card = ctk.CTkFrame(self, fg_color="transparent")
            card.grid(row=0, column=i, padx=10, pady=15)

            value_label = ctk.CTkLabel(card, text="0", font=("Poppins", 28, "bold"), text_color=color)
            value_label.pack()

            desc_label = ctk.CTkLabel(card, text=label, font=("Roboto", 12), text_color="#6c757d")
            desc_label.pack()

            self.stats_labels[label] = value_label

    def update_stats(self, stats_data):
        """Refresh the numbers shown on each card."""
        self.stats_labels["Total Tasks"].configure(text=str(stats_data["total"]))
        self.stats_labels["Completed"].configure(text=str(stats_data["completed"]))
        self.stats_labels["Pending"].configure(text=str(stats_data["pending"]))
        self.stats_labels["High Priority"].configure(text=str(stats_data["high_priority"]))