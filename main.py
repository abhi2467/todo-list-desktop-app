"""
To-Do List Application - Main Entry Point

This script launches the desktop version of the To‑Do List app using
CustomTkinter. It sets the global appearance and starts the main window.
"""

import customtkinter as ctk
from app import TodoApp


def main():
    """Configure the theme and run the application."""
    # Use a light colour scheme 
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")   # blue 

    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()