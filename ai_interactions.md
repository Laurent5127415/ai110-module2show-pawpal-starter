# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to add persistence to PawPal+ by saving pets and tasks to `data.json`, implement JSON serialization/deserialization methods in `pawpal_system.py`, wire the Streamlit app to load/save that state, and add a third scheduling capability beyond basic sorting/conflict detection.

**What did the agent do?**

- Edited `pawpal_system.py` to support `Owner.to_dict()`, `Pet.to_dict()`, `Task.to_dict()`, and matching `from_dict()` methods.
- Added `Scheduler.save_to_json()` and `Scheduler.load_from_json()` to persist data.
- Added `Scheduler.find_next_available_time_slot()` as a new algorithmic capability.
- Updated `app.py` to load `data.json` at startup, save state after adding pets/tasks, and expose the next available time slot search.
- Added `tests/test_persistence.py` to validate JSON persistence and the slot-finding logic.

**What did you have to verify or fix manually?**

- Verified the JSON serialization logic could round-trip correctly, especially `datetime` fields.
- Confirmed the app saved state after task creation and loaded it on restart.
- Ensured `Scheduler.load_from_json()` correctly rebuilt owner/pet/task relationships.
- Added documentation for the persistence workflow and clarified that a custom dict conversion approach was used instead of `marshmallow`.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Copilot-style code assistant | ChatGPT-style reasoning assistant |
| **Prompt** | "Implement robust weekly recurrence rescheduling logic for recurring tasks so that completing a weekly task creates the next occurrence exactly 7 days later, avoids duplicates, and handles timezone/date arithmetic cleanly." | "Design the algorithm for rescheduling weekly recurring tasks after completion, including edge cases like a task completed late, duplicate task creation, and preserving weekly cadence." |
| **Response summary** | Gave a concise implementation sketch with direct Python code for `mark_done()` and `find_next_available_time_slot()` logic. | Provided a more detailed reasoning path, describing edge cases and recommending a separate helper for date calculation and duplicate checks. |
| **What was useful** | Quick code-ready answer and a clear implementation path for the scheduler method. | Better explanation of edge cases, including late completion and ensuring the next occurrence is based on the original recurrence interval. |
| **Problems noticed** | Under-emphasized the duplicate task prevention and handling of already-completed tasks in the same week. | More verbose and less immediately code-ready, requiring extra pruning to fit the project style. |
| **Decision** | Not chosen for final implementation. | Chosen as the primary design influence. |

**Which approach did you use in your final implementation and why?**

I used the ChatGPT-style reasoning assistant as the main design influence because it gave stronger guidance on weekly recurrence edge cases and made the final code more robust. The Copilot-style answer was useful for quick code structure, but the final scheduler logic benefited from the higher-level validation and duplicate prevention that came from the reasoning-focused response.
