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

Run the full test suite with:

```bash
python -m pytest
```

This project includes tests for:

- task sorting by chronological order,
- recurring task creation when a daily task is completed,
- duplicate-time conflict detection for tasks scheduled at the same time,
- basic pet/task object behavior and scheduler filtering.

Successful test output:

```text
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/laurentshumbusha/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 7 items                                                               

tests/test_pawpal.py .....                                               [ 71%]
tests/test_pawpal_system.py ..                                           [100%]

============================== 7 passed in 0.02s ===============================
```

**Confidence Level:** ★★★★☆

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
| **Next Available Slot** | `Scheduler.find_next_available_time_slot(duration_minutes, after=None)` | Finds the earliest available start time after a given datetime where a new task can fit without overlapping existing incomplete tasks. Useful for suggesting open scheduling windows. |
| **Recurring Tasks** | `Task.mark_done()` with `frequency` field | Tasks can be marked "daily" or "weekly". When marked complete, automatically creates a new instance for the next occurrence using `timedelta(days=1)` or `timedelta(days=7)`. One-time tasks return `None`. |

## Persistence Workflow

The app now persists owner, pet, and task state to `data.json` between runs. The following files were modified for persistence:

- `pawpal_system.py` — added `save_to_json` and `load_from_json` methods, plus object serialization/deserialization helpers for `Owner`, `Pet`, and `Task`.
- `app.py` — loads saved state at startup and saves state after new pets or tasks are added.
- `tests/test_persistence.py` — verifies JSON save/load and the new next-available-slot feature.

The persistence implementation uses a custom dictionary conversion pattern rather than an external library like `marshmallow`. Each class converts to a JSON-safe dict using `to_dict()`, and `from_dict()` rebuilds objects with proper `datetime` parsing.

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

## CLI Formatting Enhancements

The CLI runner now uses `tabulate` to print structured tables and `colorama` for color-coded status indicators. Tasks are shown with emojis based on type, such as:

- `🐾` for walks
- `🍽️` for feeding
- `💊` for medical tasks
- `✂️` for grooming
- `🎾` for play

Priority values are printed in color:

- red for High
- cyan for Medium
- blue for Low

Output is generated in `main.py` using:

- `tabulate` for pretty table formatting
- `colorama` for ANSI color styling

The status column also includes friendly symbols and text:

- `✓ Completed`
- `○ Pending`

| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

### Main UI features

- Add a pet with name, species, and age.
- Select a pet and create a care task with time, duration, priority, and task type.
- View the selected pet's task table with completion status and recurrence details.
- Generate the day's schedule using priority-based scheduling with `Scheduler.sort_by_priority()`.
- See conflict warnings from `Scheduler.check_for_warnings()` for overlapping or exact-time tasks.

### CLI Output Example

When the scheduler orders tasks by priority first, then by time, the output looks like:

```text
Today's Schedule
================
- 08:00 | Mochi | Morning walk | high priority
- 09:00 | Luna | Medication | high priority
- 10:30 | Mochi | Grooming | medium priority
- 12:00 | Luna | Feed dinner | low priority
```

Tasks with the same priority are still sorted chronologically, and high-priority tasks appear before medium and low tasks.

### Example workflow

1. Open the app and confirm the owner's name and contact info.
2. Add a new pet, such as Mochi the dog.
3. Select Mochi and add a task like Morning walk at 08:00.
4. Add another task for the same or a different pet.
5. Click "Generate Schedule" to show your sorted plan and any warnings.

### Key scheduler behaviors shown

- **Sorting by time**: The schedule is presented chronologically.
- **Conflict warnings**: Warnings appear for exact-time collisions and overlapping same-pet tasks.
- **Recurring tasks**: Daily tasks can generate the next occurrence automatically when completed.
- **Task status**: The app shows pending/completed state and recurrence frequency in task tables.

### Sample CLI output

```text
======================================================================
TEST 1: All Tasks (Initial)
======================================================================
○ | 08:00 | Mochi    | Morning walk         | high     | [daily]
○ | 08:00 | Luna     | Play session         | high     | 
○ | 10:30 | Luna     | Groom Luna           | low      | 
○ | 12:00 | Mochi    | Lunch                | high     | [weekly]
○ | 18:00 | Luna     | Feed dinner          | medium   | [daily]

======================================================================
TEST 2: Conflict & Simultaneous Task Detection
======================================================================
⚠️  SIMULTANEOUS WARNING: 'Morning walk' (for Mochi) and 'Play session' (for Luna) are both scheduled at 08:00

======================================================================
TEST 3: Complete Daily Task → New Instance Created
======================================================================
Before: Morning walk @ 2026-06-25 08:00
✓ Marked as complete!
After: New instance created @ 2026-06-26 08:00

All tasks after completion:
✓ | 08:00 | Mochi    | Morning walk         | [daily]
○ | 08:00 | Luna     | Play session         | 
○ | 10:30 | Luna     | Groom Luna           | 
○ | 12:00 | Mochi    | Lunch                | [weekly]
○ | 18:00 | Luna     | Feed dinner          | [daily]
○ | 08:00 | Mochi    | Morning walk         | [daily]

======================================================================
TEST 4: Complete Weekly Task → New Instance Created
======================================================================
Before: Lunch @ 2026-06-25 12:00
✓ Marked as complete!
After: New instance created @ 2026-07-02 12:00 (+7 days)

All tasks after completion:
✓ | 08:00 | Mochi    | Morning walk         | [daily]
○ | 08:00 | Luna     | Play session         | 
○ | 10:30 | Luna     | Groom Luna           | 
✓ | 12:00 | Mochi    | Lunch                | [weekly]
○ | 18:00 | Luna     | Feed dinner          | [daily]
○ | 08:00 | Mochi    | Morning walk         | [daily]
○ | 12:00 | Mochi    | Lunch                | [weekly]

======================================================================
TEST 5: Incomplete Tasks Only
======================================================================
○ | 08:00 | Luna     | Play session         | 
○ | 10:30 | Luna     | Groom Luna           | 
○ | 18:00 | Luna     | Feed dinner          | [daily]
○ | 08:00 | Mochi    | Morning walk         | [daily]
○ | 12:00 | Mochi    | Lunch                | [weekly]

======================================================================
TEST 6: Completed Tasks Only
======================================================================
✓ | 08:00 | Mochi    | Morning walk         | [daily]
✓ | 12:00 | Mochi    | Lunch                | [weekly]
```

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