# To Do List App – Desktop Task Manager

A modern, feature‑rich task management application built with **Python** and **CustomTkinter**.  
Keep track of your tasks, set priorities, export/import data via JSON, and enjoy a clean user interface with real‑time statistics.

![Main Window](screenshots/main_window.png)  
*Main application window with task list, statistics, filters and file management.*

---

## Table of Contents

- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🛠️ Requirements & Dependencies](#️-requirements--dependencies)
- [🚀 Installation & Setup](#-installation--setup)
- [▶️ Running the Application](#️-running-the-application)
- [📸 Screenshots](#-screenshots)
- [📖 Usage Guide](#-usage-guide)
- [📦 Data Storage](#-data-storage)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

- **Add / Edit / Delete** tasks with **Low**, **Medium** or **High** priority
- **Mark tasks as completed** with a single click
- **Filter tasks** – All, Pending, Completed, High priority
- **Real‑time statistics** – total, completed, pending, and high‑priority tasks
- **Local JSON storage** – your data stays on your machine, no cloud required
- **Export / Import** tasks to/from JSON files (backup or transfer)
- **JSON preview modal** – view the raw JSON structure and copy it to clipboard
- **Help & About dialogs** – multi‑tab help guide and application info
- **Responsive layout** – adapts to window resizing
- **Keyboard shortcuts** – press `Enter` to quickly add a task

---

## 📁 Project Structure

```
todo-list-app/
│
├── main.py                 # Application entry point
├── app.py                  # Main TodoApp class (UI logic & callbacks)
├── requirements.txt        # Dependencies (customtkinter)
├── tasks.json              # Default task storage file (auto‑created)
│
├── models/                 # Data model layer
│   ├── __init__.py
│   └── task.py             # Task dataclass (serialisation to/from dict)
│
├── components/             # Reusable UI building blocks
│   ├── __init__.py
│   ├── header.py           # Title and tagline
│   ├── stats.py            # Four statistic cards
│   ├── input_section.py    # Text entry + priority buttons
│   ├── task_list.py        # Scrollable list of task widgets
│   ├── file_manager.py     # Export / Import / Preview / Clear controls
│   ├── footer.py           # Footer with Help / About links
│   └── modals.py           # JSON preview, Help, and About modal dialogs
│
└── screenshots/            # Demo screenshots (used in this README)
    ├── main_window.png
    ├── dialog_view_json.png
    ├── dialog_help_view.png
    └── dialog_about_view.png
```

---

## 🛠️ Requirements & Dependencies

- **Python 3.8+**
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) – modern UI widgets for Tkinter

All required packages are listed in `requirements.txt`.

---

## 🚀 Installation & Setup

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/todo-list-app.git
cd todo-list-app
```

Or simply extract the ZIP archive containing all the files.

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install customtkinter directly:

```bash
pip install customtkinter
```

> **Note:** `customtkinter` is the only external dependency – everything else uses Python’s standard library.

---

## ▶️ Running the Application

Make sure you are in the project’s root directory (where `main.py` is located) and run:

```bash
python main.py
```

The main window will open with a light theme.  
If no `tasks.json` file exists, the app will start with an empty task list.

---

## 📸 Screenshots

Here are some screenshots of the application in action:

| Main window | JSON preview modal |
|-------------|--------------------|
| ![Main Window](screenshots/main_window.png) | ![JSON Preview](screenshots/dialog_view_json.png) |

| Help modal (multi‑tab) | About modal |
|------------------------|--------------|
| ![Help View](screenshots/dialog_help_view.png) | ![About View](screenshots/dialog_about_view.png) |

> **Tip:** The actual screenshots will be available once you run the app and capture your own – or they can be placed in the `screenshots/` folder.

---

## 📖 Usage Guide

### Adding a task

- Type your task into the text field at the top.
- Choose a priority (**Low**, **Medium**, **High**).
- Click **Add Task** or press **Enter**.

### Managing tasks

- **Complete** a task – click the checkbox next to it.
- **Edit** a task – click the ✏️ pencil icon and modify the text in the popup.
- **Delete** a task – click the 🗑️ trash icon and confirm.

### Filtering tasks

Use the buttons above the task list:

- **All Tasks** – show everything
- **Pending** – only incomplete tasks
- **Completed** – only finished tasks
- **High Priority** – only tasks with high priority

### File management

- **Export to JSON** – save all tasks (plus metadata) to a file of your choice.
- **Import from JSON** – load tasks from a previously exported file (replace or merge).
- **View JSON Data** – opens a modal with pretty‑printed JSON; you can copy it to clipboard.
- **Clear All Tasks** – removes every task after confirmation.

### Help & About

- **Help & Guide** – a tabbed modal with Getting Started, Features, Shortcuts, FAQ, and Tips.
- **About** – version info, feature list, and technology stack.

### Notifications

Whenever you add, edit, delete, import, export or clear tasks, a temporary toast‑like message appears at the top of the window.

---

## 📦 Data Storage

- By default, tasks are saved in **`tasks.json`** (located in the same folder as `main.py`).
- The file is automatically created/updated every time you add, edit, delete, import or clear tasks.
- The JSON format is simple: an array of task objects with fields `text`, `priority`, `completed`, `created_at`, `due_date`, `id`.

Example entry:

```json
{
  "text": "Review pull requests",
  "priority": "high",
  "completed": true,
  "created_at": "2026-05-10T09:30:00",
  "due_date": null,
  "id": "a1b2c3d4-1111-2222-3333-aaaaaaaaaaaa"
}
```

> You can also export tasks with richer metadata (version, generation timestamp, totals).  
> The import function handles both the simple list format and the extended metadata format.

---
