from datetime import datetime

from colorama import Fore, Style, init
from tabulate import tabulate

from pawpal_system import Owner, Pet, Scheduler, Task


def styled_status(task: Task) -> str:
    if task.is_complete():
        return f"{Fore.GREEN}✓ Completed{Style.RESET_ALL}"
    return f"{Fore.YELLOW}○ Pending{Style.RESET_ALL}"


def task_type_icon(task_type: str) -> str:
    icons = {
        "walk": "🐾",
        "feeding": "🍽️",
        "medical": "💊",
        "grooming": "✂️",
        "play": "🎾",
    }
    return icons.get(task_type.lower(), "📝")


def styled_priority(priority: str) -> str:
    mapping = {
        "high": Fore.RED + "High" + Style.RESET_ALL,
        "medium": Fore.CYAN + "Medium" + Style.RESET_ALL,
        "low": Fore.BLUE + "Low" + Style.RESET_ALL,
    }
    return mapping.get(priority.lower(), priority.capitalize())


def build_task_row(task: Task) -> dict:
    return {
        "Status": styled_status(task),
        "Time": task.scheduled_time.strftime("%H:%M"),
        "Pet": task.pet.name,
        "Task": f"{task_type_icon(task.task_type)} {task.name}",
        "Priority": styled_priority(task.priority),
        "Frequency": task.frequency if task.frequency != "once" else "",
    }


def main() -> None:
    init(autoreset=True)

    owner = Owner("Jordan", "jordan@example.com")

    pet_one = Pet("Mochi", "dog", 3, owner)
    pet_two = Pet("Luna", "cat", 2, owner)

    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    # Create tasks with different frequencies and some at the same time
    tasks = [
        Task(
            name="Morning walk",
            duration=30,
            priority="high",
            scheduled_time=datetime(2026, 6, 25, 8, 0),
            task_type="walk",
            pet=pet_one,
            frequency="daily",
        ),
        Task(
            name="Play session",
            duration=20,
            priority="high",
            scheduled_time=datetime(2026, 6, 25, 8, 0),
            task_type="play",
            pet=pet_two,
            frequency="once",
        ),
        Task(
            name="Lunch",
            duration=15,
            priority="high",
            scheduled_time=datetime(2026, 6, 25, 12, 0),
            task_type="feeding",
            pet=pet_one,
            frequency="weekly",
        ),
        Task(
            name="Groom Luna",
            duration=45,
            priority="low",
            scheduled_time=datetime(2026, 6, 25, 10, 30),
            task_type="grooming",
            pet=pet_two,
            frequency="once",
        ),
        Task(
            name="Feed dinner",
            duration=15,
            priority="medium",
            scheduled_time=datetime(2026, 6, 25, 18, 0),
            task_type="feeding",
            pet=pet_two,
            frequency="daily",
        ),
    ]

    for task in tasks:
        task.pet.add_task(task)

    scheduler = Scheduler([pet_one, pet_two])

    print("=" * 70)
    print("TEST 1: All Tasks (Initial)")
    print("=" * 70)
    all_tasks = scheduler.sort_by_time()
    print(tabulate([build_task_row(task) for task in all_tasks], headers="keys", tablefmt="fancy_grid"))

    print("\n" + "=" * 70)
    print("TEST 2: Conflict & Simultaneous Task Detection")
    print("=" * 70)
    warnings = scheduler.check_for_warnings()
    if warnings:
        for warning in warnings:
            print(f"{Fore.RED}{warning}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✓ No conflicts detected.{Style.RESET_ALL}")

    print("\n" + "=" * 70)
    print("TEST 3: Complete Daily Task → New Instance Created")
    print("=" * 70)
    morning_walk = tasks[0]
    print(f"Before: {morning_walk.name} @ {morning_walk.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    new_task = morning_walk.mark_done()
    print(f"{Fore.GREEN}✓ Marked as complete!{Style.RESET_ALL}")
    if new_task:
        print(f"After: New instance created @ {new_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")

    print("\nAll tasks after completion:")
    scheduler = Scheduler([pet_one, pet_two])
    all_tasks = scheduler.sort_by_time()
    print(tabulate([build_task_row(task) for task in all_tasks], headers="keys", tablefmt="fancy_grid"))

    print("\n" + "=" * 70)
    print("TEST 4: Complete Weekly Task → New Instance Created")
    print("=" * 70)
    lunch_task = tasks[2]
    print(f"Before: {lunch_task.name} @ {lunch_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    new_task = lunch_task.mark_done()
    print(f"{Fore.GREEN}✓ Marked as complete!{Style.RESET_ALL}")
    if new_task:
        print(f"After: New instance created @ {new_task.scheduled_time.strftime('%Y-%m-%d %H:%M')} (+7 days)")

    print("\nAll tasks after completion:")
    scheduler = Scheduler([pet_one, pet_two])
    all_tasks = scheduler.sort_by_time()
    print(tabulate([build_task_row(task) for task in all_tasks], headers="keys", tablefmt="fancy_grid"))

    print("\n" + "=" * 70)
    print("TEST 5: Incomplete Tasks Only")
    print("=" * 70)
    incomplete = scheduler.filter_by_completion(False)
    print(tabulate([build_task_row(task) for task in sorted(incomplete, key=lambda t: t.scheduled_time)], headers="keys", tablefmt="fancy_grid"))

    print("\n" + "=" * 70)
    print("TEST 6: Completed Tasks Only")
    print("=" * 70)
    completed = scheduler.filter_by_completion(True)
    print(tabulate([build_task_row(task) for task in sorted(completed, key=lambda t: t.scheduled_time)], headers="keys", tablefmt="fancy_grid"))


if __name__ == "__main__":
    main()
