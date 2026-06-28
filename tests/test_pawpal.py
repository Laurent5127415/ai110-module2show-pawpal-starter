from datetime import datetime

from pawpal_system import Owner, Pet, Task


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
