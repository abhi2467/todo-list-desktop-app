"""
Modal dialogs used throughout the app:
- JSON preview (view/copy the raw JSON)
- Help (multi‑tab guide)
- About (version and credits)
"""

import customtkinter as ctk
import json
from datetime import datetime
import tkinter as tk


class BaseModal:
    """Base class that handles showing/hiding a modal window."""

    def __init__(self, parent):
        self.parent = parent
        self.modal = None

    def show(self, data=None):
        """Bring the modal to the front; create it if it doesn't exist."""
        if not self.modal or not self.modal.winfo_exists():
            self.create_modal(data)
        else:
            self.modal.lift()
            self.modal.focus()

    def create_modal(self, data=None):
        """Override in subclasses to build the specific modal content."""
        pass

    def hide(self):
        """Close and destroy the modal window."""
        if self.modal and self.modal.winfo_exists():
            self.modal.destroy()
            self.modal = None


class JsonPreviewModal(BaseModal):
    """Modal that displays the current tasks as formatted JSON and allows copying."""

    def create_modal(self, data=None):
        self.modal = ctk.CTkToplevel(self.parent)
        self.modal.title("JSON File Preview")
        self.modal.geometry("800x600")
        self.modal.transient(self.parent)
        self.modal.grab_set()          # make it modal

        # Header with title
        header_frame = ctk.CTkFrame(self.modal, fg_color="#4b6cb7", corner_radius=0)
        header_frame.pack(fill="x")
        title_label = ctk.CTkLabel(
            header_frame,
            text="JSON File Preview",
            font=("Poppins", 20, "bold"),
            text_color="white"
        )
        title_label.pack(pady=20)

        # Main content area
        content_frame = ctk.CTkFrame(self.modal)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Read‑only text widget for the JSON
        json_text = tk.Text(
            content_frame,
            font=("Courier", 12),
            wrap="word",
            bg="#f8f9fa",
            fg="#343a40",
            relief="flat",
            padx=10,
            pady=10
        )
        json_text.pack(fill="both", expand=True, pady=(0, 10))

        json_str = ""
        if data:
            json_str = json.dumps(data, indent=2, default=str)
            json_text.insert("1.0", json_str)
            json_text.configure(state="disabled")

        # Buttons row
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x")

        copy_btn = ctk.CTkButton(
            button_frame,
            text="Copy JSON",
            font=("Roboto", 14),
            height=40,
            command=lambda s=json_str: self.copy_json(s)
        )
        copy_btn.pack(side="left", padx=5)

        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            font=("Roboto", 14),
            height=40,
            fg_color="#6c757d",
            command=self.hide
        )
        close_btn.pack(side="right", padx=5)

    def copy_json(self, json_str):
        """Copy the JSON text to the system clipboard and show a temporary success message."""
        try:
            self.parent.clipboard_clear()
            self.parent.clipboard_append(json_str)
            success_label = ctk.CTkLabel(
                self.modal,
                text="JSON copied to clipboard!",
                text_color="#28a745",
                font=("Roboto", 12)
            )
            success_label.place(relx=0.5, y=560, anchor="center")
            self.modal.after(2000, success_label.destroy)
        except Exception as e:
            print(f"Clipboard error: {e}")


class HelpModal(BaseModal):
    """A tabbed help window with Getting Started, Features, Shortcuts, FAQ, Tips."""

    def create_modal(self, data=None):
        self.modal = ctk.CTkToplevel(self.parent)
        self.modal.title("Help & Guide")
        self.modal.geometry("900x700")
        self.modal.transient(self.parent)
        self.modal.grab_set()

        self.tabview = ctk.CTkTabview(self.modal)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Create all tabs
        self.tabview.add("Getting Started")
        self.tabview.add("Features")
        self.tabview.add("Shortcuts")
        self.tabview.add("FAQ")
        self.tabview.add("Tips & Tricks")

        # Fill each tab with content
        self.fill_getting_started_tab()
        self.fill_features_tab()
        self.fill_shortcuts_tab()
        self.fill_faq_tab()
        self.fill_tips_tab()

    def fill_getting_started_tab(self):
        tab = self.tabview.tab("Getting Started")
        title = ctk.CTkLabel(tab, text="Welcome to To Do List App",
                             font=("Poppins", 20, "bold"), text_color="#182848")
        title.pack(pady=(10, 20))

        content = """
1. Adding Tasks
• Type your task in the input field at the top
• Select a priority level (Low, Medium, or High)
• Click "Add Task" or press Enter

2. Managing Tasks
• Click checkbox to mark tasks complete
• Use edit button to modify tasks
• Use delete button to remove tasks
• Filter tasks using the filter buttons

3. File Management
• Export tasks to JSON file for backup
• Import tasks from JSON file
• View tasks in JSON format
• Clear all tasks when needed
"""
        label = ctk.CTkLabel(tab, text=content, font=("Roboto", 14),
                             text_color="#6c757d", justify="left")
        label.pack(padx=20, pady=10, fill="both", expand=True)

    def fill_features_tab(self):
        tab = self.tabview.tab("Features")
        features = [
            "✓ Smart Task Creation with priority levels",
            "✓ Advanced Filtering by status and priority",
            "✓ Real-time Statistics dashboard",
            "✓ Data Export/Import using JSON files",
            "✓ Responsive Design for all devices",
            "✓ Visual Priority indicators",
            "✓ Auto Save functionality",
            "✓ Local Storage for privacy"
        ]
        for f in features:
            ctk.CTkLabel(tab, text=f, font=("Roboto", 14),
                         text_color="#6c757d", justify="left").pack(anchor="w", padx=20, pady=5)

    def fill_shortcuts_tab(self):
        tab = self.tabview.tab("Shortcuts")
        shortcuts = [
            "Enter - Add a new task",
            "Tab - Navigate between elements",
            "Ctrl+Enter - Quick add task",
            "Escape - Close modals",
            "Ctrl+S / Cmd+S - Quick save/export",
            "Ctrl+F / Cmd+F - Focus on search"
        ]
        for s in shortcuts:
            ctk.CTkLabel(tab, text=s, font=("Roboto", 14),
                         text_color="#6c757d", justify="left").pack(anchor="w", padx=20, pady=5)

    def fill_faq_tab(self):
        tab = self.tabview.tab("FAQ")
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", expand=True)

        faqs = [
            ("Q: Where are my tasks stored?",
             "A: Your tasks are stored locally in a JSON file on your computer."),
            ("Q: How do I backup my tasks?",
             "A: Use the 'Export to JSON' button to save your tasks to a file."),
            ("Q: Can I use the app offline?",
             "A: Yes! The app works completely offline."),
            ("Q: How do I clear all tasks?",
             "A: Use the 'Clear All Tasks' button in the File Management section."),
            ("Q: Can I change task priority?",
             "A: Yes! Edit the task to change its priority level.")
        ]
        for q, a in faqs:
            ctk.CTkLabel(scroll, text=q, font=("Roboto", 14, "bold"),
                         text_color="#182848", justify="left").pack(anchor="w", padx=20, pady=(10, 0))
            ctk.CTkLabel(scroll, text=a, font=("Roboto", 13),
                         text_color="#6c757d", justify="left", wraplength=700).pack(anchor="w", padx=20, pady=(0, 10))

    def fill_tips_tab(self):
        tab = self.tabview.tab("Tips & Tricks")
        tips = [
            "• Use priority levels to categorize tasks effectively",
            "• Break large projects into smaller tasks",
            "• Review and prioritize your task list daily",
            "• Export your tasks weekly for backup",
            "• Use filters for different working modes",
            "• Learn keyboard shortcuts for faster workflow"
        ]
        for tip in tips:
            ctk.CTkLabel(tab, text=tip, font=("Roboto", 14),
                         text_color="#6c757d", justify="left").pack(anchor="w", padx=20, pady=5)


class AboutModal(BaseModal):
    """Modal with version, description, features and technology stack used."""

    def create_modal(self, data=None):
        self.modal = ctk.CTkToplevel(self.parent)
        self.modal.title("About To Do List")
        self.modal.geometry("600x500")
        self.modal.transient(self.parent)
        self.modal.grab_set()

        # Blue header
        header = ctk.CTkFrame(self.modal, fg_color="#4b6cb7", corner_radius=0)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="About To Do List", font=("Poppins", 20, "bold"),
                     text_color="white").pack(pady=20)

        content = ctk.CTkFrame(self.modal)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(content, text="Version 1.0.0", font=("Poppins", 16, "bold"),
                     text_color="#182848").pack(pady=(10, 5))
        ctk.CTkLabel(content, text="A simple, powerful task management application\nbuilt with CustomTkinter and Python.",
                     font=("Roboto", 14), text_color="#6c757d").pack(pady=(0, 20))

        # Features list
        ctk.CTkLabel(content, text="Features:", font=("Roboto", 14, "bold"),
                     text_color="#182848").pack(anchor="w", padx=20, pady=(10, 5))
        features = [
            "• Local storage for privacy and offline use",
            "• JSON import/export for data portability",
            "• Priority-based task organization",
            "• Real-time statistics and filtering",
            "• Responsive design"
        ]
        for f in features:
            ctk.CTkLabel(content, text=f, font=("Roboto", 13),
                         text_color="#6c757d", justify="left").pack(anchor="w", padx=40, pady=2)

        # Technology stack
        ctk.CTkLabel(content, text="Technology:", font=("Roboto", 14, "bold"),
                     text_color="#182848").pack(anchor="w", padx=20, pady=(20, 5))
        tech = [
            "• Built with Python and CustomTkinter",
            "• Uses JSON files for data persistence",
            "• No external dependencies required"
        ]
        for t in tech:
            ctk.CTkLabel(content, text=t, font=("Roboto", 13),
                         text_color="#6c757d", justify="left").pack(anchor="w", padx=40, pady=2)

        ctk.CTkLabel(content, text="© 2025 To Do List App | All Rights Reserved",
                     font=("Roboto", 12), text_color="#adb5bd").pack(side="bottom", pady=20)