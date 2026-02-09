"""
PawPal+ Demo Script
Demonstrates the scheduling system with a realistic daily scenario
"""

from pawpal_system import Owner, Pet, Task, TaskType, Priority, Scheduler


def print_header(title: str) -> None:
    """Print a formatted header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_schedule(schedule: list[tuple]) -> None:
    """Print the schedule in a formatted table"""
    if not schedule:
        print("No tasks scheduled.")
        return

    print(f"{'TIME':<10} | {'TASK':<30} | {'PET':<15} | {'DURATION':<10}")
    print("-" * 70)

    for task, start_time in schedule:
        print(
            f"{start_time:<10} | {task.title:<30} | {task.pet_name:<15} | "
            f"{task.duration_minutes}min"
        )

    print()


def print_reasoning(reasoning: list[str]) -> None:
    """Print scheduling reasoning line by line"""
    print("SCHEDULING REASONING:")
    print("-" * 70)
    for line in reasoning:
        print(f"  {line}")
    print()


def main():
    """Main demo function"""

    print_header("PawPal+ Daily Schedule Demo")

    # ===== SET UP OWNER =====
    print("Setting up owner and pets...")
    owner = Owner(name="Jordan", available_time_minutes=180)
    print(f"✓ Owner: {owner.name} with {owner.available_time_minutes} minutes available")

    # ===== SET UP PETS =====
    mochi = Pet(name="Mochi", species="dog", age=3, energy_level="high")
    luna = Pet(name="Luna", species="cat", age=7, energy_level="medium")

    owner.add_pet(mochi)
    owner.add_pet(luna)

    print(f"✓ Pet 1: {mochi.name} ({mochi.species}, age {mochi.age})")
    print(f"✓ Pet 2: {luna.name} ({luna.species}, age {luna.age})")

    # ===== ADD TASKS FOR MOCHI (DOG) =====
    mochi.add_task(
        Task(
            title="Morning walk",
            task_type=TaskType.WALK,
            duration_minutes=30,
            priority=Priority.HIGH,
            time_preference="morning",
        )
    )
    mochi.add_task(
        Task(
            title="Feed Mochi",
            task_type=TaskType.FEEDING,
            duration_minutes=10,
            priority=Priority.HIGH,
        )
    )
    mochi.add_task(
        Task(
            title="Playtime",
            task_type=TaskType.ENRICHMENT,
            duration_minutes=20,
            priority=Priority.MEDIUM,
        )
    )
    mochi.add_task(
        Task(
            title="Evening walk",
            task_type=TaskType.WALK,
            duration_minutes=30,
            priority=Priority.HIGH,
        )
    )

    # ===== ADD TASKS FOR LUNA (CAT) =====
    luna.add_task(
        Task(
            title="Thyroid medication",
            task_type=TaskType.MEDICATION,
            duration_minutes=5,
            priority=Priority.HIGH,
            time_preference="morning",
        )
    )
    luna.add_task(
        Task(
            title="Feed Luna",
            task_type=TaskType.FEEDING,
            duration_minutes=10,
            priority=Priority.HIGH,
        )
    )
    luna.add_task(
        Task(
            title="Litter box cleaning",
            task_type=TaskType.ENRICHMENT,
            duration_minutes=15,
            priority=Priority.MEDIUM,
        )
    )
    luna.add_task(
        Task(
            title="Grooming",
            task_type=TaskType.GROOMING,
            duration_minutes=20,
            priority=Priority.LOW,
        )
    )
    luna.add_task(
        Task(
            title="Play with toys",
            task_type=TaskType.ENRICHMENT,
            duration_minutes=15,
            priority=Priority.MEDIUM,
        )
    )

    print(f"✓ Added {len(mochi.tasks)} tasks for {mochi.name}")
    print(f"✓ Added {len(luna.tasks)} tasks for {luna.name}")

    # ===== CALCULATE TOTAL CARE TIME =====
    mochi_total = mochi.calculate_total_care_time()
    luna_total = luna.calculate_total_care_time()
    total_needed = mochi_total + luna_total

    print(f"\nTotal care time needed:")
    print(f"  - {mochi.name}: {mochi_total} minutes")
    print(f"  - {luna.name}: {luna_total} minutes")
    print(f"  - Total: {total_needed} minutes")
    print(f"  - Available: {owner.available_time_minutes} minutes")

    # ===== GENERATE SCHEDULE =====
    print_header("Generating Daily Schedule")

    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()

    # ===== PRINT SCHEDULE =====
    print("TODAY'S SCHEDULE:")
    print_schedule(schedule)

    # ===== PRINT REASONING =====
    print_reasoning(scheduler.get_reasoning())

    # ===== DEMONSTRATE TASK COMPLETION =====
    print_header("Task Completion Tracking Demo")

    if schedule:
        first_task_title = schedule[0][0].title
        print(f"Marking '{first_task_title}' as completed...")
        scheduler.mark_task_complete(first_task_title)

        remaining = scheduler.get_remaining_tasks()
        print(f"Remaining tasks: {len(remaining)}")
        for task, time in remaining:
            print(f"  - {time}: {task.title}")
    else:
        print("No tasks scheduled to mark complete.")

    # ===== SHOW HIGH PRIORITY TASKS =====
    print_header("High Priority Tasks Summary")

    all_high_priority = []
    for pet in owner.get_all_pets():
        high_tasks = pet.get_high_priority_tasks()
        for task in high_tasks:
            all_high_priority.append((pet.name, task))

    if all_high_priority:
        print(f"Found {len(all_high_priority)} high-priority tasks:\n")
        for pet_name, task in all_high_priority:
            print(f"  {pet_name}: {task.title} ({task.duration_minutes}min)")
    else:
        print("No high-priority tasks found.")

    print("\n" + "=" * 70)
    print("  Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
