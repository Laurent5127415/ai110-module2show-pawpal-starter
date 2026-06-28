# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design had four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` holds owner details and a list of pets. `Pet` stores pet details and a list of tasks. `Task` captures task metadata such as name, duration, priority, scheduled time, type, and completion state. `Scheduler` collects tasks from all pets and organizes them into a daily plan.

- What classes did you include, and what responsibilities did you assign to each?

A user should be able to:
1. enter owner and pet details,
2. add pet care tasks with schedule, priority, and recurrence,
3. view a daily plan sorted by time,
4. receive warnings for conflicting tasks.

`Owner` manages pets. `Pet` manages tasks. `Task` represents a single care action and stores its own completion state. `Scheduler` handles task collection, sorting, filtering, conflict detection, and warning generation.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design evolved. I added a `pet` reference inside `Task` so each task is explicitly associated with a pet. I also added `completed` and `frequency` fields to `Task` to support recurring tasks and completion tracking. In `Scheduler`, I added methods for sorting by time, filtering by completion or pet, and detecting both overlapping and simultaneous tasks. I chose to keep `Pet.owner` required so every pet is always tied to an owner in the system.

### Building blocks

- `Owner` class
  - `add_pet()`
  - `get_all_pets()`
- `Pet` class
  - `add_task()`
  - `get_tasks()`
- `Task` class
  - `is_complete()`
  - `mark_done()`
  - `frequency` field for recurring tasks
- `Scheduler` class
  - `generate_schedule()`
  - `sort_by_time()`
  - `filter_by_completion()`
  - `filter_by_pet()`
  - `detect_conflicts()`
  - `detect_simultaneous_tasks()`
  - `check_for_warnings()`

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers time, priority, completion state, and recurrence. Time and priority are the most important constraints: the schedule must be ordered chronologically, and higher-priority tasks should be easier to spot. Completion state ensures done tasks can be filtered out, while `frequency` supports repeated care like daily or weekly tasks.

I chose these constraints because they reflect the core use case of the app: a task must occur at the right time, urgent care should be visible, and recurring tasks should not need manual re-entry.

**b. Tradeoffs**

The scheduler makes a tradeoff between **simplicity and precision in conflict detection**:

- **Tradeoff**: `detect_simultaneous_tasks()` flags only tasks with the exact same start time, not tasks that partially overlap with different start times.
- **Why reasonable**: This keeps the warning system useful without overwhelming the user, while `detect_conflicts()` still catches same-pet overlaps.
- **Trade-off detail**: The system focuses on the most important conflicts, such as double-booking the same pet or two tasks that start at the same time, instead of attempting exhaustive overlap analysis across all pets.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI for design brainstorming, implementation guidance, debugging, and writing tests. Helpful prompts included asking for:
- scheduler method implementations,
- recurrence handling with `timedelta`,
- conflict detection strategies,
- Streamlit UI patterns for schedule display.

These prompts helped break the project into concrete backend and UI work and allowed me to implement the core features faster.

**b. Judgment and verification**

I did not accept every AI suggestion as-is. For example, I rejected a suggestion to use a complex generic constraint dictionary or `TypeDict` for scheduler rules because that would have added unnecessary complexity for the current scope.

I verified suggestions by reviewing the logic manually, checking that it matched the app requirements, and running tests. For example, I confirmed recurrence behavior by marking a daily task complete and verifying that a new task was created for the next day.

---

## 4. Testing and Verification

**a. What you tested**

I tested the scheduler's core behaviors:
- chronological sorting of tasks,
- recurrence creation after marking a task complete,
- conflict detection for simultaneous tasks,
- basic task completion handling.

These tests were important because they cover the main app behaviors: ordered schedule generation, repeatable care, and conflict awareness.

**b. Confidence**

I am fairly confident in the current implementation. The core scheduler logic is covered and the app can build schedules and warn on conflicts.

If I had more time, I would add tests for:
- partial overlaps across different pets,
- multiple simultaneous tasks,
- recurrence edge cases at midnight or month boundaries,
- invalid time input,
- Streamlit state persistence across sessions.

---

## 5. Reflection

**a. What went well**

The clean separation between backend scheduler logic and the Streamlit UI went well. The scheduler is reusable and the UI simply displays the results.

**b. What you would improve**

If I had another iteration, I would improve conflict detection to handle more overlap cases consistently and add richer task editing and persistence in the UI.

**c. Key takeaway**

I learned that AI is a strong implementation partner, but final architecture and tradeoff decisions must remain with the developer. Effective AI collaboration means verifying suggestions with tests and choosing the simplest design that meets the needs.
