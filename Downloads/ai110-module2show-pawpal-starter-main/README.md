# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

---

## Smarter Scheduling (Phase 4)

PawPal+ includes intelligent algorithmic features to make pet care planning more efficient:

### 🔢 **Sorting by Time**
View your daily schedule in chronological order, regardless of how tasks were added or prioritized.

```python
sorted_schedule = scheduler.sort_by_time()
```

- **Algorithm:** Uses Python's Timsort (O(n log n))
- **Converts:** Time strings ("9:00 AM") to comparable integers
- **Handles:** 12-hour format edge cases (12 AM, 12 PM)

### 🔍 **Filtering Tasks**
Focus on specific pets or task statuses:

```python
# Show only tasks for a specific pet
mochi_tasks = scheduler.filter_by_pet("Mochi")

# Show only incomplete tasks
incomplete = scheduler.filter_by_status(completed=False)
```

- **Algorithm:** List comprehensions (O(n))
- **Use cases:** Pet-specific views, completion tracking, progress reports

### 🔄 **Recurring Tasks**
Daily and weekly tasks automatically recreate themselves when completed:

```python
# Create recurring task
task = Task(
    title="Daily feeding",
    task_type=TaskType.FEEDING,
    duration_minutes=10,
    priority=Priority.HIGH,
    frequency="daily"  # or "weekly"
)

# When marked complete, next day's task is auto-created
scheduler.mark_task_complete("Daily feeding")
```

- **Algorithm:** Template pattern with `datetime.timedelta`
- **Supported:** Daily (+1 day), Weekly (+7 days)
- **Benefits:** Reduces repetitive data entry, ensures consistency

### ⚠️ **Conflict Detection**
Automatically detects when tasks overlap in time:

```python
conflicts = scheduler.detect_conflicts()
# Returns: ["⚠ Conflict: 'Walk' (9:00 AM) overlaps with 'Feed' (9:30 AM)"]
```

- **Algorithm:** Pairwise interval overlap check (O(n²))
- **Detects:** Tasks with overlapping time windows
- **Returns:** Warning messages instead of preventing scheduling
- **Tradeoff:** User autonomy over strict validation

---

## Running the App

### Demo Script (CLI)
```bash
python main.py
```

Demonstrates:
- Multi-pet scheduling with priorities
- Task completion tracking
- Sorting, filtering, recurring tasks, conflict detection

### Streamlit UI
```bash
streamlit run app.py
```

Open browser to `http://localhost:8501` for interactive experience:
- Add pets and tasks through web interface
- Generate schedules with visual feedback
- Track completion with real-time metrics
- View reasoning and conflicts

### Run Tests
```bash
pytest tests/ -v
```

**Expected:** 35 passed (10 Phase 1 + 18 Phase 2 + 7 Phase 4)

---

## Project Structure

```
pawpal-main/
├── pawpal_system.py          # Core logic (Owner, Pet, Task, Scheduler)
├── app.py                     # Streamlit UI with session state
├── main.py                    # CLI demo script
├── tests/
│   ├── test_pawpal_system.py  # Phase 1: Instantiation tests
│   ├── test_pawpal.py         # Phase 2: Functionality tests
│   └── test_pawpal_phase4.py  # Phase 4: Algorithm tests
├── reflection.md              # Design documentation & analysis
├── PHASE_3_INTEGRATION.md     # UI integration guide
├── INTEGRATION_CHECKLIST.md   # Verification checklist
└── PHASE_3_SUMMARY.md         # Phase 3 overview
```

---

## Features Implemented

### Phase 1: System Design ✅
- UML class diagram with relationships
- TaskType and Priority enums
- Task, Pet, Owner, Scheduler classes
- 10 unit tests

### Phase 2: Core Logic ✅
- 18 method implementations (Pet: 6, Owner: 5, Scheduler: 7+3)
- Greedy scheduling algorithm (O(n log n))
- Priority-based task selection
- Transparent reasoning engine
- 18 comprehensive tests

### Phase 3: UI Integration ✅
- Streamlit session state management
- Full CRUD operations (Create, Read, Update, Delete)
- Real-time calculations and metrics
- Task completion tracking
- Integration documentation

### Phase 4: Smart Algorithms ✅
- Time-based sorting
- Pet/status filtering
- Recurring task automation
- Conflict detection
- 7 algorithm-specific tests

---

## Algorithm Complexity Analysis

| Feature | Time Complexity | Space Complexity |
|---------|----------------|------------------|
| Greedy Scheduling | O(n log n) | O(n) |
| Time Sorting | O(n log n) | O(n) |
| Filtering | O(n) | O(k) |
| Recurring Tasks | O(1) | O(1) |
| Conflict Detection | O(n²) | O(c) |

*Where n = total tasks, k = filtered results, c = conflicts found*

---

## Contributing

This is an educational project for AI110 Module 2. All phases completed:
- ✅ OOP design principles applied
- ✅ Comprehensive testing suite
- ✅ Clean separation of concerns (logic vs. UI)
- ✅ Algorithmic thinking and tradeoff analysis

---

## License

Educational project - Howard University AI110 Course
