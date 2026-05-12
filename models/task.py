"""
Task data model – defines what a single task looks like.

Uses a dataclass to reduce boilerplate. Handles serialisation to/from
dictionaries (for JSON storage).
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Task:
    """Represents one to‑do item with text, priority, completion status, dates, and a unique ID."""

    text: str
    priority: str = "medium"            # low, medium, high
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        """Convert the task into a JSON‑serialisable dictionary."""
        data = asdict(self)
        # Convert datetime objects to ISO format strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Recreate a Task object from a dictionary (e.g., loaded from JSON)."""
        # Turn ISO date strings back into datetime objects
        for date_field in ['created_at', 'due_date']:
            if date_field in data and data[date_field]:
                try:
                    data[date_field] = datetime.fromisoformat(data[date_field])
                except (ValueError, TypeError):
                    data[date_field] = None
        return cls(**data)