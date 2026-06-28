from datetime import datetime, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_changes_status():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)
    task = Task(
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="walk",
        pet=pet,
    )

    assert task.is_complete() is False

    task.mark_done()

    assert task.is_complete() is True


def test_adding_task_increases_pet_task_count():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)
    task = Task(
        name="Feed dinner",
        duration=15,
        priority="medium",
        scheduled_time=datetime(2026, 6, 25, 18, 0),
        task_type="feeding",
        pet=pet,
    )

    assert len(pet.get_tasks()) == 0

    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)

    task_a = Task(
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 10, 0),
        task_type="walk",
        pet=pet,
    )
    task_b = Task(
        name="Lunch",
        duration=15,
        priority="medium",
        scheduled_time=datetime(2026, 6, 25, 12, 0),
        task_type="feeding",
        pet=pet,
    )
    task_c = Task(
        name="Breakfast",
        duration=10,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="feeding",
        pet=pet,
    )

    pet.add_task(task_a)
    pet.add_task(task_b)
    pet.add_task(task_c)

    scheduler = Scheduler([pet])
    sorted_tasks = scheduler.sort_by_time()

    assert [task.name for task in sorted_tasks] == ["Breakfast", "Morning walk", "Lunch"]


def test_mark_done_daily_creates_new_task_for_next_day():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)

    task = Task(
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="walk",
        pet=pet,
        frequency="daily",
    )
    pet.add_task(task)

    new_task = task.mark_done()

    assert task.is_complete() is True
    assert new_task is not None
    assert new_task.frequency == "daily"
    assert new_task.scheduled_time.date() == task.scheduled_time.date() + timedelta(days=1)
    assert new_task in pet.get_tasks()


def test_detect_simultaneous_tasks_flags_duplicate_start_time():
    owner = Owner("Jordan", "jordan@example.com")
    pet_one = Pet("Mochi", "dog", 3, owner)
    pet_two = Pet("Luna", "cat", 2, owner)

    task_one = Task(
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="walk",
        pet=pet_one,
    )
    task_two = Task(
        name="Play session",
        duration=20,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="play",
        pet=pet_two,
    )

    pet_one.add_task(task_one)
    pet_two.add_task(task_two)

    scheduler = Scheduler([pet_one, pet_two])
    simultaneous = scheduler.detect_simultaneous_tasks()

    assert len(simultaneous) == 1
    assert simultaneous[0] == (task_one, task_two)
