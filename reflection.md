# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My initial design has four classes. The Owner class holds information about the pet owner and links to their pets. The Pet class stores each pet's details and connects to that pet's list of care tasks. The Task class is a dataclass that holds all the details about a single care activity - its name, duration, priority, scheduled time, and type. Finally, the Scheduler class si responsible for taking all the tasks and organizing them into a logical daily plan, checking for conflicts and sorting by priority. 

- What classes did you include, and what responsibilities did you assign to each?

A user should be able to: (1) enter their pet's name and type, (2) add tasks like feeding or walking with a time and priority level, and (3) see a daily plan showing all tasks in order.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After asking the AI to review my skeleton, I made several changes. First, I added a pet attribute to the Task dataclass so that each task knows which pet it belongs to - without this, there was no way to answer 'whose task is this?" without searching every pet's list. Second, I added a completed: bool = false field to Task because the original skeleton had is_complete () and mark_done() methods but no actual attribute to store whether the task was done. Third, I added a pet(s) lists to the Scheduler class so it has context about all pets when building the daily plan, not jsut a flat list of disconnected task type values are restricted to a known set of options, which prevents typos. I chose not to implement TypeDict for the constraints dictionary since that is advanced Python, but I added comments explaining what keys it should contain. I also kept the owner field in Pet as required rather than optional, since every pet in this system must belong to an owener. 

STEP 2: List the Building Blocks
Owner class
    -Name: add_per()
    -contact_info: get_all_pets()
Pet class
    -Name: add_task()
    -Species(dogs, cat...): get_tasks()
    -Age
    -Owner
Task class
    -Name ("Morning walk"): Is_complete()
    -Duration (in minutes): mark_done()
    -priority (high/medium/low)
    -scheduled_time
    -Task_type (walk/feed/med..)
scheduler class
    -Tasks (a list): generate_schedule()
    -Constraints: Sort_by_priority() / detect_conflicts()



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler makes an important tradeoff between **simplicity and precision in conflict detection**:

- **Tradeoff**: The `detect_simultaneous_tasks()` method flags only tasks with **exact same start times**, not overlapping durations. For example, a task from 08:00-08:30 and another from 08:15-08:45 for the *same pet* will be detected by `detect_conflicts()` (overlap detection), but two tasks at exactly 08:00 (one for Mochi, one for Luna) will be detected by `detect_simultaneous_tasks()`.

- **Why reasonable**: This tradeoff allows the scheduler to:
  1. Quickly identify critical conflicts (owner can't supervise two pets at the exact same time)
  2. Still catch resource conflicts (same pet doing two things at once via `detect_conflicts()`)
  3. Remain non-blocking—warnings are returned, not exceptions, so the app continues functioning
  
- **Trade-off detail**: The approach sacrifices 100% conflict detection (e.g., it won't flag tasks for different pets that partially overlap but don't start at the same time) for **usability**. In practice, the owner would want to notice that both pets need attention at 08:00, but might be okay with one task running 08:00-08:30 and another running 08:15-09:00 if they're for different pets. This keeps the UI from becoming overwhelmed with warnings.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
