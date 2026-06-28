from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", "jordan@example.com")

    pet_one = Pet("Mochi", "dog", 3, owner)
    pet_two = Pet("Luna", "cat", 2, owner)

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    # Create tasks with different frequencies and some at the same time
    tasks = [
        # Morning walk for Mochi (daily recurring)
        Task(
            name="Morning walk",
            duration=30,
            priority="high",
            scheduled_time=datetime(2026, 6, 25, 8, 0),
            task_type="walk",
            pet=pet_one,
            frequency="daily",  # This will recur daily
        ),
        # Luna's playtime at the same time (SIMULTANEOUS CONFLICT!)
        Task(
            name="Play session",
            duration=20,
            priority="high",
            scheduled_time=datetime(2026, 6, 25, 8, 0),
            task_type="play",
            pet=pet_two,
            frequency="once",
        ),
        # Lunch for Mochi (weekly recurring)
        Task(
            name="Lunch",
            duration=15,
            priority="high",
            scheduled_time=datetime(2026, 6, 25, 12, 0),
            task_type="feeding",
            pet=pet_one,
            frequency="weekly",  # This will recur weekly
        ),
        # Groom Luna (one-time task)
        Task(
            name="Groom Luna",
            duration=45,
            priority="low",
            scheduled_time=datetime(2026, 6, 25, 10, 30),
            task_type="grooming",
            pet=pet_two,
            frequency="once",
        ),
        # Feed Luna dinner (daily recurring)
        Task(
            name="Feed dinner",
            duration=15,
            priority="medium",
            scheduled_time=datetime(2026, 6, 25, 18, 0),
            task_type="feeding",
            pet=pet_two,
            frequency="daily",  # This will recur daily
        ),
    ]

    for task in tasks:
        task.pet.add_task(task)

    scheduler = Scheduler([pet_one, pet_two])

    # ===== TEST 1: Display all tasks before any completion =====
    print("=" * 70)
    print("TEST 1: All Tasks (Initial)")
    print("=" * 70)
    all_tasks = scheduler.sort_by_time()
    for task in all_tasks:
        status = "✓" if task.is_complete() else "○"
        freq = f"[{task.frequency}]" if task.frequency != "once" else ""
        print(
            f"{status} | {task.scheduled_time.strftime('%H:%M')} | {task.pet.name:8} | {task.name:20} | {task.priority:8} | {freq}"
        )

    # ===== TEST 2: Check for warnings (conflicts) =====
    print("\n" + "=" * 70)
    print("TEST 2: Conflict & Simultaneous Task Detection")
    print("=" * 70)
    warnings = scheduler.check_for_warnings()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("✓ No conflicts detected.")

    # ===== TEST 3: Mark a daily task as complete (creates new instance) =====
    print("\n" + "=" * 70)
    print("TEST 3: Complete Daily Task → New Instance Created")
    print("=" * 70)
    morning_walk = tasks[0]  # Morning walk (daily)
    print(f"Before: {morning_walk.name} @ {morning_walk.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    new_task = morning_walk.mark_done()
    print(f"✓ Marked as complete!")
    if new_task:
        print(f"After: New instance created @ {new_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    
    # Display all tasks after marking one complete
    print("\nAll tasks after completion:")
    scheduler = Scheduler([pet_one, pet_two])  # Refresh scheduler
    all_tasks = scheduler.sort_by_time()
    for task in all_tasks:
        status = "✓" if task.is_complete() else "○"
        freq = f"[{task.frequency}]" if task.frequency != "once" else ""
        print(
            f"{status} | {task.scheduled_time.strftime('%H:%M')} | {task.pet.name:8} | {task.name:20} | {freq}"
        )

    # ===== TEST 4: Mark a weekly task as complete =====
    print("\n" + "=" * 70)
    print("TEST 4: Complete Weekly Task → New Instance Created")
    print("=" * 70)
    lunch_task = tasks[2]  # Lunch (weekly)
    print(f"Before: {lunch_task.name} @ {lunch_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    new_task = lunch_task.mark_done()
    print(f"✓ Marked as complete!")
    if new_task:
        print(f"After: New instance created @ {new_task.scheduled_time.strftime('%Y-%m-%d %H:%M')} (+7 days)")
    
    # Display all tasks after completing another one
    print("\nAll tasks after completion:")
    scheduler = Scheduler([pet_one, pet_two])  # Refresh scheduler
    all_tasks = scheduler.sort_by_time()
    for task in all_tasks:
        status = "✓" if task.is_complete() else "○"
        freq = f"[{task.frequency}]" if task.frequency != "once" else ""
        print(
            f"{status} | {task.scheduled_time.strftime('%H:%M')} | {task.pet.name:8} | {task.name:20} | {freq}"
        )

    # ===== TEST 5: Filter completed vs incomplete =====
    print("\n" + "=" * 70)
    print("TEST 5: Incomplete Tasks Only")
    print("=" * 70)
    incomplete = scheduler.filter_by_completion(False)
    for task in sorted(incomplete, key=lambda t: t.scheduled_time):
        freq = f"[{task.frequency}]" if task.frequency != "once" else ""
        print(
            f"○ | {task.scheduled_time.strftime('%H:%M')} | {task.pet.name:8} | {task.name:20} | {freq}"
        )

    print("\n" + "=" * 70)
    print("TEST 6: Completed Tasks Only")
    print("=" * 70)
    completed = scheduler.filter_by_completion(True)
    for task in sorted(completed, key=lambda t: t.scheduled_time):
        freq = f"[{task.frequency}]" if task.frequency != "once" else ""
        print(
            f"✓ | {task.scheduled_time.strftime('%H:%M')} | {task.pet.name:8} | {task.name:20} | {freq}"
        )


if __name__ == "__main__":
    main()
