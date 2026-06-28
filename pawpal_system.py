import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import combinations
from typing import List, Optional


class Owner:
    """Represents a pet owner."""

    def __init__(self, name: str, contact_info: str):
        """Initialize an owner with a name and contact information."""
        self.name = name
        self.contact_info = contact_info
        self.pets: List['Pet'] = []

    def add_pet(self, pet: 'Pet') -> None:
        """Add a pet to this owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)

    def get_all_pets(self) -> List['Pet']:
        """Return all pets owned by this owner."""
        return list(self.pets)

    def remove_pet(self, pet: 'Pet') -> None:
        """Remove a pet from this owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)

    def to_dict(self) -> dict:
        """Serialize this owner and its nested pets to a dictionary."""
        return {
            "name": self.name,
            "contact_info": self.contact_info,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Owner':
        """Deserialize an owner and nested pets from a dictionary."""
        owner = cls(name=data["name"], contact_info=data.get("contact_info", ""))
        for pet_data in data.get("pets", []):
            pet = Pet.from_dict(pet_data, owner)
            owner.add_pet(pet)
        return owner


@dataclass
class Pet:
    """Represents a pet owned by an owner."""

    name: str
    species: str
    age: int
    owner: Owner

    def __post_init__(self):
        """Initialize the pet's task list after creation."""
        self.tasks: List['Task'] = []

    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)

    def get_tasks(self) -> List['Task']:
        """Return all tasks assigned to this pet."""
        return list(self.tasks)

    def remove_task(self, task: 'Task') -> None:
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def to_dict(self) -> dict:
        """Serialize this pet and its tasks to a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict, owner: 'Owner') -> 'Pet':
        """Deserialize a pet and its tasks from a dictionary."""
        pet = cls(
            name=data["name"],
            species=data.get("species", ""),
            age=data.get("age", 0),
            owner=owner,
        )
        for task_data in data.get("tasks", []):
            task = Task.from_dict(task_data, pet)
            pet.add_task(task)
        return pet


@dataclass
class Task:
    """Represents a task to be scheduled for a pet."""

    name: str
    duration: float
    priority: str
    scheduled_time: datetime
    task_type: str
    pet: 'Pet'
    completed: bool = False
    completed_time: Optional[datetime] = None
    frequency: str = "once"  # "once", "daily", "weekly"

    def is_complete(self) -> bool:
        """Return whether this task has been completed."""
        return self.completed

    def mark_done(self) -> Optional['Task']:
        """Mark this task as complete and record when it was finished.
        
        If the task is recurring (daily/weekly), automatically creates and returns
        a new instance for the next occurrence. Otherwise, returns None.
        
        Returns:
            A new Task instance if recurring, None if one-time task.
        """
        self.completed = True
        self.completed_time = datetime.now()
        
        # Handle recurring tasks
        if self.frequency == "daily":
            next_scheduled = self.scheduled_time + timedelta(days=1)
            new_task = Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                scheduled_time=next_scheduled,
                task_type=self.task_type,
                pet=self.pet,
                completed=False,
                completed_time=None,
                frequency="daily"
            )
            self.pet.add_task(new_task)
            return new_task
        
        elif self.frequency == "weekly":
            next_scheduled = self.scheduled_time + timedelta(days=7)
            new_task = Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                scheduled_time=next_scheduled,
                task_type=self.task_type,
                pet=self.pet,
                completed=False,
                completed_time=None,
                frequency="weekly"
            )
            self.pet.add_task(new_task)
            return new_task
        
        return None

    def to_dict(self) -> dict:
        """Serialize this task to a dictionary."""
        return {
            "name": self.name,
            "duration": self.duration,
            "priority": self.priority,
            "scheduled_time": self.scheduled_time.isoformat(),
            "task_type": self.task_type,
            "completed": self.completed,
            "completed_time": self.completed_time.isoformat() if self.completed_time else None,
            "frequency": self.frequency,
        }

    @classmethod
    def from_dict(cls, data: dict, pet: 'Pet') -> 'Task':
        """Deserialize a task from a dictionary."""
        completed_time = data.get("completed_time")
        return cls(
            name=data["name"],
            duration=float(data.get("duration", 0.0)),
            priority=data.get("priority", "low"),
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]),
            task_type=data.get("task_type", "other"),
            pet=pet,
            completed=data.get("completed", False),
            completed_time=datetime.fromisoformat(completed_time) if completed_time else None,
            frequency=data.get("frequency", "once"),
        )


class Scheduler:
    """Manages and schedules tasks for pets."""

    def __init__(self, pets: Optional[List[Pet]] = None, constraints: Optional[dict] = None):
        """Initialize the scheduler with optional pets and constraints."""
        self.pets = pets or []
        self.tasks: List[Task] = []
        self.constraints = constraints or {}

    def _collect_tasks(self) -> List[Task]:
        """Collect tasks from all pets managed by the scheduler."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def generate_schedule(self) -> List[Task]:
        """Create a schedule from all collected tasks."""
        self.tasks = self._collect_tasks()
        return list(self.tasks)

    def sort_by_priority(self) -> List[Task]:
        """Sort tasks by their priority level."""
        self.tasks = self.generate_schedule()
        priority_rank = {"low": 0, "medium": 1, "high": 2}
        return sorted(
            self.tasks,
            key=lambda task: (
                -priority_rank.get(task.priority.lower(), 0),
                task.scheduled_time,
            ),
        )

    def sort_by_time(self) -> List[Task]:
        """Sort tasks chronologically by their scheduled time (earliest first)."""
        self.tasks = self.generate_schedule()
        return sorted(self.tasks, key=lambda task: task.scheduled_time)

    def filter_by_completion(self, completed: bool) -> List[Task]:
        """Filter tasks by completion status.
        
        Args:
            completed: If True, return completed tasks. If False, return incomplete tasks.
            
        Returns:
            List of tasks matching the completion status.
        """
        all_tasks = self.generate_schedule()
        return [task for task in all_tasks if task.is_complete() == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks by pet name.
        
        Args:
            pet_name: The name of the pet to filter by.
            
        Returns:
            List of tasks assigned to the specified pet.
        """
        all_tasks = self.generate_schedule()
        return [task for task in all_tasks if task.pet.name.lower() == pet_name.lower()]

    def detect_conflicts(self) -> List:
        """Detect overlapping tasks for the same pet (time-based conflicts).
        
        Uses interval overlap detection: task1 overlaps with task2 if task1 starts
        before task2 ends AND task2 starts before task1 ends.
        
        Returns:
            List of tuples (task1, task2) where both tasks are for the same pet
            and their scheduled times overlap based on duration.
            
        Example:
            A task from 08:00-08:30 and another from 08:15-08:45 will be flagged.
            A task from 08:00-08:30 and another from 08:30-09:00 will NOT be flagged (adjacent is OK).
        """
        tasks = self.generate_schedule()
        conflicts = []
        
        for task1, task2 in combinations(tasks, 2):
            # Only check conflicts for tasks belonging to the same pet
            if task1.pet != task2.pet:
                continue

            # Calculate end times for both tasks
            task1_end = task1.scheduled_time + timedelta(minutes=task1.duration)
            task2_end = task2.scheduled_time + timedelta(minutes=task2.duration)
            
            # Interval overlap formula: A starts before B ends AND B starts before A ends
            overlaps = (
                task1.scheduled_time < task2_end and task2.scheduled_time < task1_end
            )
            
            if overlaps:
                conflicts.append((task1, task2))
        
        return conflicts
    
    def detect_simultaneous_tasks(self) -> List[tuple]:
        """Detect tasks scheduled at the exact same time (across all pets).
        
        This checks for exact time matches, not overlapping durations. Useful for
        identifying scheduling conflicts where two tasks start simultaneously but
        may be for different pets.
        
        Returns:
            List of tuples (task1, task2) representing tasks scheduled at the same time.
            
        Example:
            Morning walk at 08:00 and Play session at 08:00 -> flagged
            Morning walk at 08:00 and Play session at 08:10 -> not flagged
        """
        tasks = self.generate_schedule()
        
        # Use combinations to get all unique pairs without duplication
        return [
            (task1, task2)
            for task1, task2 in combinations(tasks, 2)
            if task1.scheduled_time == task2.scheduled_time
        ]
    
    def check_for_warnings(self) -> List[str]:
        """Generate warning messages for conflicts and simultaneous tasks.
        
        This is a lightweight, non-blocking conflict detection strategy that returns
        human-readable warning messages instead of raising exceptions. Allows the
        scheduler to continue operating while alerting the user to potential issues.
        
        Checks for two types of problems:
        1. Overlapping tasks for the same pet (time-based conflicts)
        2. Multiple tasks scheduled at the exact same time (across any pets)
        
        Returns:
            List of warning message strings. Empty list if no conflicts detected.
            
        Example:
            [
                '⚠️  OVERLAP WARNING: Morning walk and Vet appointment overlap for Mochi (08:00 - 08:45)',
                '⚠️  SIMULTANEOUS WARNING: Morning walk (for Mochi) and Play session (for Luna) are both scheduled at 08:00'
            ]
        """
        warnings = []
        
        # Check for overlapping tasks on the same pet (temporal conflicts)
        conflicts = self.detect_conflicts()
        for task1, task2 in conflicts:
            task1_end = (task1.scheduled_time + timedelta(minutes=task1.duration)).strftime('%H:%M')
            warning = (
                f"⚠️  OVERLAP WARNING: '{task1.name}' and '{task2.name}' "
                f"overlap for {task1.pet.name} "
                f"({task1.scheduled_time.strftime('%H:%M')} - {task1_end})"
            )
            warnings.append(warning)
        
        # Check for simultaneous tasks (exact time matches across pets)
        simultaneous = self.detect_simultaneous_tasks()
        for task1, task2 in simultaneous:
            warning = (
                f"⚠️  SIMULTANEOUS WARNING: '{task1.name}' (for {task1.pet.name}) and "
                f"'{task2.name}' (for {task2.pet.name}) are both scheduled at {task1.scheduled_time.strftime('%H:%M')}"
            )
            warnings.append(warning)
        
        return warnings

    def find_next_available_time_slot(
        self, duration_minutes: int, after: Optional[datetime] = None
    ) -> Optional[datetime]:
        """Find the next free time slot for a new task.

        Scans existing incomplete tasks and returns the earliest start time after `after`
        where a new task of `duration_minutes` can fit without overlapping.
        """
        if duration_minutes <= 0:
            return None

        search_start = after or datetime.now()
        tasks = sorted(
            [task for task in self.generate_schedule() if not task.completed],
            key=lambda task: task.scheduled_time,
        )
        candidate = search_start

        for task in tasks:
            task_start = task.scheduled_time
            task_end = task_start + timedelta(minutes=task.duration)
            candidate_end = candidate + timedelta(minutes=duration_minutes)

            if candidate_end <= task_start:
                return candidate

            if task_start <= candidate < task_end:
                candidate = task_end
            elif candidate < task_start < candidate_end:
                candidate = task_end

        return candidate

    def save_to_json(self, path: str = "data.json") -> None:
        """Serialize the current owner/pet/task state to a JSON file."""
        owners_by_name = {}
        for pet in self.pets:
            owner = pet.owner
            if owner.name not in owners_by_name:
                owners_by_name[owner.name] = owner

        data = {
            "owners": [owner.to_dict() for owner in owners_by_name.values()]
        }

        with open(path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2)

    @classmethod
    def load_from_json(cls, path: str = "data.json") -> 'Scheduler':
        """Load scheduler state from a JSON file."""
        if not os.path.exists(path):
            return cls()

        with open(path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)

        owners = [Owner.from_dict(owner_data) for owner_data in data.get("owners", [])]
        pets: List[Pet] = []
        for owner in owners:
            pets.extend(owner.get_all_pets())

        scheduler = cls(pets=pets)
        return scheduler
