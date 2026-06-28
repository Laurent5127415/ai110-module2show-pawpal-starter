from datetime import datetime
import os
import json

from pawpal_system import Owner, Pet, Scheduler, Task

DATA_PATH = "test_data.json"


def teardown_module(module):
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)


def test_save_and_load_scheduler_state():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)
    owner.add_pet(pet)

    task = Task(
        name="Feed dinner",
        duration=15,
        priority="medium",
        scheduled_time=datetime(2026, 6, 25, 18, 0),
        task_type="feeding",
        pet=pet,
    )
    pet.add_task(task)

    scheduler = Scheduler(pets=[pet])
    scheduler.save_to_json(DATA_PATH)

    assert os.path.exists(DATA_PATH)

    with open(DATA_PATH, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    assert data["owners"][0]["name"] == "Jordan"
    assert data["owners"][0]["pets"][0]["name"] == "Mochi"
    assert data["owners"][0]["pets"][0]["tasks"][0]["name"] == "Feed dinner"

    loaded_scheduler = Scheduler.load_from_json(DATA_PATH)
    assert len(loaded_scheduler.pets) == 1
    loaded_pet = loaded_scheduler.pets[0]
    assert loaded_pet.name == "Mochi"
    assert len(loaded_pet.get_tasks()) == 1
    assert loaded_pet.get_tasks()[0].name == "Feed dinner"


def test_find_next_available_time_slot():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", 3, owner)
    owner.add_pet(pet)

    task1 = Task(
        name="Morning walk",
        duration=30,
        priority="high",
        scheduled_time=datetime(2026, 6, 25, 8, 0),
        task_type="walk",
        pet=pet,
    )
    task2 = Task(
        name="Feeding",
        duration=20,
        priority="medium",
        scheduled_time=datetime(2026, 6, 25, 8, 45),
        task_type="feeding",
        pet=pet,
    )
    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler([pet])
    next_slot = scheduler.find_next_available_time_slot(30, after=datetime(2026, 6, 25, 8, 0))

    assert next_slot == datetime(2026, 6, 25, 9, 5)
