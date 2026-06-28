# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The scheduler script was run successfully and produced the following terminal output:

```text
Today's Schedule
================
- 08:00 | Mochi | Morning walk | high priority
- 14:00 | Luna | Play session | high priority
- 18:00 | Mochi | Feed dinner | medium priority
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

Your **PawPal+ Scheduler** now includes several algorithmic features for intelligent task management:

| Feature | Method(s) | Description |
|---------|-----------|-------------|
| **Chronological Sorting** | `Scheduler.sort_by_time()` | Sorts all tasks by their `scheduled_time` (earliest first). Uses Python's `sorted()` with a lambda key. Returns tasks in chronological order for display in the daily plan. |
| **Priority-Based Sorting** | `Scheduler.sort_by_priority()` | Sorts tasks by priority level (high → medium → low) with ties broken by scheduled time. Creates a priority ranking dictionary and uses multi-key sorting. |
| **Filter by Completion** | `Scheduler.filter_by_completion(completed: bool)` | Returns either completed or incomplete tasks. Uses list comprehension to check `task.is_complete()` status. Useful for showing "To-Do" vs "Done" lists. |
| **Filter by Pet** | `Scheduler.filter_by_pet(pet_name: str)` | Returns all tasks assigned to a specific pet by name (case-insensitive). Useful for viewing one pet's schedule independently. |
| **Overlap Detection** | `Scheduler.detect_conflicts()` | Identifies tasks for the **same pet** that have overlapping time intervals. Uses interval overlap formula: `task1_start < task2_end AND task2_start < task1_end`. Accounts for task duration. |
| **Simultaneous Task Detection** | `Scheduler.detect_simultaneous_tasks()` | Identifies tasks scheduled at the **exact same time** (across all pets). Uses `itertools.combinations()` for clean pair iteration. Helps detect when owner attention is divided. |
| **Lightweight Conflict Warnings** | `Scheduler.check_for_warnings()` | Returns a list of human-readable warning messages for both overlaps and simultaneous tasks. Non-blocking strategy—app continues running even when conflicts exist. |
| **Recurring Tasks** | `Task.mark_done()` with `frequency` field | Tasks can be marked "daily" or "weekly". When marked complete, automatically creates a new instance for the next occurrence using `timedelta(days=1)` or `timedelta(days=7)`. One-time tasks return `None`. |

### Example Usage

```python
# Create and populate scheduler
scheduler = Scheduler(pets=[mochi, luna])

# Sort and display
chronological = scheduler.sort_by_time()
print(f"Daily plan: {len(chronological)} tasks")

# Get warnings
warnings = scheduler.check_for_warnings()
if warnings:
    for warning in warnings:
        print(warning)  # ⚠️ OVERLAP WARNING: ...

# Filter tasks
mochi_tasks = scheduler.filter_by_pet("Mochi")
incomplete = scheduler.filter_by_completion(False)

# Handle recurring tasks
morning_walk = tasks[0]  # daily task
new_instance = morning_walk.mark_done()  # creates tomorrow's walk
```
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->




Mermaid Liver Editor diagram code: 

classDiagram
    class Owner {
        -name: str
        -contact_info: str
        +add_pet(pet: Pet)
void
        +get_all_pets()
list[Pet]
    }
    
    class Pet {
        -name: str
        -species: str
        -age: int
        -owner: Owner
        +add_task(task: Task)
void
        +get_tasks()
list[Task]
    }
    
    class Task {
        -name: str
        -duration: float
        -priority: str
        -scheduled_time: datetime
        -task_type: str
        +is_complete()
bool
        +mark_done()
void
    }
    
    class Scheduler {
        -tasks: list[Task]
        -constraints: dict
        +generate_schedule()
list[Task]
        +sort_by_priority()
list[Task]
        +detect_conflicts()
list
    }
    
    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler --> "*" Task : manages