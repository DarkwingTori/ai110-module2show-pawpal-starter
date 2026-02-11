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

## Key Features

### 🐾 Pet Management
- ✅ Multi-pet support (dogs, cats, birds, rabbits, and more)
- ✅ Pet-specific task lists with independent management
- ✅ Energy level tracking (low, medium, high)
- ✅ Special needs accommodation

### 📋 Task Scheduling
- ✅ Priority-based scheduling (HIGH, MEDIUM, LOW)
- ✅ Time constraint enforcement (respects owner's available time)
- ✅ Morning/evening time preferences
- ✅ Transparent reasoning engine (explains every decision)
- ✅ Greedy first-fit algorithm (O(n log n))

### 🤖 Smart Algorithms (Phase 4)
- ✅ **Chronological sorting** - View tasks in time order
- ✅ **Pet-specific filtering** - Focus on one pet at a time
- ✅ **Completion status filtering** - Track progress
- ✅ **Recurring tasks** - Daily/weekly tasks auto-recreate when completed
- ✅ **Conflict detection** - Identify overlapping time windows

### 💻 User Interface
- ✅ Interactive Streamlit web app with real-time updates
- ✅ Session state management for data persistence
- ✅ Real-time metrics and calculations
- ✅ Task completion tracking with progress indicators
- ✅ Visual feedback (success messages, warnings, error handling)
- ✅ Responsive layout with sidebar navigation

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

### 📸 Demo Screenshots

![PawPal+ Streamlit Interface - Task Management](pawpal_screenshot2.png)

*Interactive Streamlit interface showing owner setup (sidebar), pet management with priority indicators (🔴 HIGH, 🟡 MEDIUM, 🟢 LOW), task assignment, and real-time metrics*

![PawPal+ Streamlit Interface - Full View](pawpal_screenshot.png)

*Complete view of PawPal+ showing task list, priority indicators, recurring task badges (🔄), and time utilization metrics*

### Run Tests
```bash
pytest tests/ -v
```

**Expected:** 35 passed (10 Phase 1 + 18 Phase 2 + 7 Phase 4)

---

## Testing PawPal+

### Test Suite Overview

PawPal+ includes a comprehensive test suite with **35 automated tests** covering all system components and algorithms.

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_pawpal_phase4.py -v

# Run with coverage report (requires pytest-cov)
python -m pytest tests/ --cov=pawpal_system
```

### Test Organization

| Test File | Tests | Coverage |
|-----------|-------|----------|
| test_pawpal_system.py | 10 | Class instantiation, enum values, mutable defaults |
| test_pawpal.py | 18 | Task management, scheduling algorithm, edge cases |
| test_pawpal_phase4.py | 7 | Sorting, filtering, recurring tasks, conflicts |
| **Total** | **35** | **Complete system coverage** |

### What We Test

#### 1. Core Functionality (Phase 1-2)
- ✅ Class instantiation and initialization
- ✅ Task priority comparison and sorting
- ✅ Pet and owner management (add, remove, get)
- ✅ Task completion tracking
- ✅ Total care time calculations

#### 2. Scheduling Algorithm (Phase 2)
- ✅ Priority-based scheduling (HIGH → MEDIUM → LOW)
- ✅ Time constraint enforcement (respects available_time_minutes)
- ✅ Time preference handling (morning tasks prioritized)
- ✅ Multi-pet scheduling coordination
- ✅ Reasoning generation for transparency

#### 3. Edge Cases (Phase 2)
- ✅ Empty task lists
- ✅ Zero available time
- ✅ No pets registered
- ✅ Invalid priority strings
- ✅ Task removal with non-existent tasks

#### 4. Smart Algorithms (Phase 4)
- ✅ Time-based sorting (chronological order)
- ✅ Pet-specific filtering
- ✅ Status-based filtering (completed/incomplete)
- ✅ Recurring task creation (daily/weekly)
- ✅ Automatic next occurrence generation
- ✅ Conflict detection (overlapping time windows)
- ✅ Adjacent task validation (no false positives)

### Test Results

```
============================== 35 passed in 0.02s ==============================

✓ Phase 1: 10/10 tests passing
✓ Phase 2: 18/18 tests passing
✓ Phase 4: 7/7 tests passing

Total: 35/35 (100%)
```

### Confidence Level: ⭐⭐⭐⭐⭐ (5/5 stars)

**Why high confidence:**

1. **Comprehensive Coverage** - All major features tested (instantiation, scheduling, algorithms, edge cases)
2. **100% Pass Rate** - All 35 tests pass consistently with fast execution (0.02s)
3. **Edge Case Handling** - Tests cover empty lists, zero time, invalid inputs, conflicts
4. **Algorithm Verification** - Sorting, filtering, recurring tasks, conflict detection all validated
5. **Real-world Testing** - main.py demo script exercises entire system end-to-end

**Known Limitations:**
- Tests assume valid input formats (time strings, dates)
- Conflict detection only checks time overlap, not resource constraints
- No stress testing for large numbers of tasks (100+)
- No integration tests for Streamlit UI components

**Next Testing Steps (if expanding):**
- Add property-based testing with Hypothesis
- Add performance benchmarks for large schedules
- Add integration tests for UI components
- Add mutation testing to verify test quality

### Example Test Output

```python
pytest tests/test_pawpal_phase4.py -v

tests/test_pawpal_phase4.py::test_sort_by_time PASSED              [14%]
tests/test_pawpal_phase4.py::test_filter_by_pet PASSED             [28%]
tests/test_pawpal_phase4.py::test_filter_by_status PASSED          [42%]
tests/test_pawpal_phase4.py::test_recurring_task_creation PASSED   [57%]
tests/test_pawpal_phase4.py::test_mark_complete_creates_recurrence PASSED [71%]
tests/test_pawpal_phase4.py::test_detect_conflicts PASSED          [85%]
tests/test_pawpal_phase4.py::test_no_conflicts_when_tasks_adjacent PASSED [100%]
```

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
