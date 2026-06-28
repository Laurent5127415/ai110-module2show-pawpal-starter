import streamlit as st
from datetime import datetime, date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Initialize session state for owner (if not already created)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", contact_info="555-1234-5678")

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

# ===== OWNER SECTION =====
st.subheader("👤 Pet Owner")
owner = st.session_state.owner
st.write(f"**Name:** {owner.name}")
st.write(f"**Contact:** {owner.contact_info}")
st.write(f"**Pets:** {len(owner.get_all_pets())} pet(s)")

# ===== ADD PET SECTION =====
st.subheader("🐾 Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi", key="pet_name_input")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], key="species_select")
with col3:
    pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3, key="pet_age_input")

if st.button("Add Pet", key="add_pet_button"):
    # Create a new Pet object and add it to the owner
    new_pet = Pet(name=pet_name, species=species, age=pet_age, owner=owner)
    owner.add_pet(new_pet)
    st.session_state.current_pet = new_pet
    st.success(f"✅ Added {pet_name} the {species}!")
    st.rerun()

# Display all pets for this owner
if owner.get_all_pets():
    st.markdown("**Your Pets:**")
    for pet in owner.get_all_pets():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🐶 **{pet.name}** ({pet.species}, {pet.age} yrs) — {len(pet.get_tasks())} task(s)")
        with col2:
            if st.button("Select", key=f"select_pet_{pet.name}"):
                st.session_state.current_pet = pet
                st.rerun()

# ===== ADD TASK SECTION =====
if st.session_state.current_pet:
    st.divider()
    current_pet = st.session_state.current_pet
    st.subheader(f"📋 Add Task for {current_pet.name}")
    
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task name", value="Morning walk", key="task_name_input")
        duration_min = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30, key="duration_input")
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority_select")
        task_type = st.selectbox("Task type", ["feeding", "exercise", "grooming", "medical", "other"], key="task_type_select")
    
    task_time = st.time_input("Scheduled time", value=None, key="task_time_input")
    
    if st.button("Add Task", key="add_task_button"):
        if task_time:
            from datetime import datetime, date
            # Combine today's date with the selected time
            scheduled_datetime = datetime.combine(date.today(), task_time)
            
            # Create Task object and add to pet
            new_task = Task(
                name=task_title,
                duration=float(duration_min),
                priority=priority,
                scheduled_time=scheduled_datetime,
                task_type=task_type,
                pet=current_pet
            )
            current_pet.add_task(new_task)
            st.success(f"✅ Added '{task_title}' for {current_pet.name}!")
            st.rerun()
        else:
            st.error("Please select a time for the task.")
    
    # Display tasks for current pet
    tasks = current_pet.get_tasks()
    if tasks:
        st.markdown(f"**Tasks for {current_pet.name}:**")
        for task in tasks:
            status = "✓" if task.is_complete() else "○"
            st.write(f"{status} **{task.name}** ({task.duration} min) — {task.priority} priority @ {task.scheduled_time.strftime('%H:%M')}")
    else:
        st.info(f"No tasks yet for {current_pet.name}. Add one above!")
else:
    st.info("👉 Please add a pet first before creating tasks.")

st.divider()

# ===== SCHEDULER SECTION =====
st.subheader("📅 Generate Schedule")
if owner.get_all_pets():
    if st.button("Generate schedule", key="generate_schedule_button"):
        # Create scheduler with all pets
        scheduler = Scheduler(pets=owner.get_all_pets())
        schedule = scheduler.generate_schedule()
        
        if schedule:
            st.success("✅ Schedule generated!")
            st.markdown("**Daily Schedule:**")
            sorted_tasks = sorted(schedule, key=lambda t: t.scheduled_time)
            for task in sorted_tasks:
                st.write(f"- **{task.scheduled_time.strftime('%H:%M')}** - {task.name} ({task.duration} min) for {task.pet.name}")
        else:
            st.info("No tasks scheduled.")
else:
    st.warning("Add a pet and tasks before generating a schedule.")
