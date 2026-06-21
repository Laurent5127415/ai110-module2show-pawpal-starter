from dataclasses import dataclass
from datetime import datetime
from typing import List


class Owner:
    """Represents a pet owner."""
    
    def __init__(self, name: str, contact_info: str):
        """Initialize an Owner with name and contact information."""
        self.name = name
        self.contact_info = contact_info
        self.pets: List['Pet'] = []
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to the owner's collection of pets."""
        pass
    
    def get_all_pets(self) -> List['Pet']:
        """Retrieve all pets owned by this owner."""
        pass


@dataclass
class Pet:
    """Represents a pet owned by an owner."""
    
    name: str
    species: str
    age: int
    owner: Owner
    
    def __post_init__(self):
        """Initialize pet tasks list after dataclass initialization."""
        self.tasks: List['Task'] = []
    
    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list."""
        pass
    
    def get_tasks(self) -> List['Task']:
        """Retrieve all tasks assigned to this pet."""
        pass


@dataclass
class Task:
    """Represents a task to be scheduled for a pet."""
    
    name: str
    duration: float
    priority: str
    scheduled_time: datetime
    task_type: str
    
    def is_complete(self) -> bool:
        """Check if the task has been completed."""
        pass
    
    def mark_done(self) -> None:
        """Mark this task as complete."""
        pass


class Scheduler:
    """Manages and schedules tasks for pets."""
    
    def __init__(self, constraints: dict = None):
        """Initialize a Scheduler with optional constraints."""
        self.tasks: List[Task] = []
        self.constraints = constraints or {}
    
    def generate_schedule(self) -> List[Task]:
        """Generate an optimized schedule from all tasks."""
        pass
    
    def sort_by_priority(self) -> List[Task]:
        """Sort all tasks by their priority level."""
        pass
    
    def detect_conflicts(self) -> List:
        """Detect any scheduling conflicts or overlaps in tasks."""
        pass
