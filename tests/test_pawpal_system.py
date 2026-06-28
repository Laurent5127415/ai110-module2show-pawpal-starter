from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def test_owner_pet_and_task_lifecycle():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)

    owner.add_pet(pet)
    assert owner.get_all_pets() == [pet]

    task = Task(
        name="Morning walk",
        duration=20,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="walk",
        pet=pet,
    )
    pet.add_task(task)
    assert pet.get_tasks() == [task]

    assert task.is_complete() is False
    task.mark_done()
    assert task.is_complete() is True

    pet.remove_task(task)
    assert pet.get_tasks() == []

    owner.remove_pet(pet)
    assert owner.get_all_pets() == []


def test_scheduler_collects_tasks_and_detects_conflicts():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)
    owner.add_pet(pet)

    task_one = Task(
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="walk",
        pet=pet,
    )
    task_two = Task(
        name="Feeding",
        duration=15,
        priority="medium",
        scheduled_time=datetime(2026, 6, 25, 8, 15),
        task_type="feeding",
        pet=pet,
    )
    pet.add_task(task_one)
    pet.add_task(task_two)

    scheduler = Scheduler([pet])
    assert scheduler.generate_schedule() == [task_one, task_two]
    assert scheduler.sort_by_priority()[0] == task_one

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert conflicts[0][0] == task_one
    assert conflicts[0][1] == task_two
