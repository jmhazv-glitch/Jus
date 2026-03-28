import pytest

try:
    from GUI.todo_app import TodoStore
except ImportError as exc:  # tkinter might be missing in headless envs
    TodoStore = None
    pytest.skip(f"todo_app import skipped: {exc}", allow_module_level=True)


def test_add_trims_and_stores_task():
    store = TodoStore()
    task = store.add("  Estudiar Tkinter  ")

    assert task is not None
    assert task.text == "Estudiar Tkinter"
    assert task.completed is False
    assert len(store.tasks) == 1


def test_add_rejects_empty_task():
    store = TodoStore()

    assert store.add("   ") is None
    assert store.tasks == []


def test_complete_marks_task_as_completed():
    store = TodoStore()
    store.add("Tarea A")

    updated = store.complete(0)

    assert updated is not None
    assert updated.completed is True
    assert store.tasks[0].completed is True


def test_delete_removes_selected_task():
    store = TodoStore()
    store.add("Tarea A")
    store.add("Tarea B")

    removed = store.delete(0)

    assert removed is not None
    assert removed.text == "Tarea A"
    assert [task.text for task in store.tasks] == ["Tarea B"]


def test_invalid_indexes_return_none():
    store = TodoStore()
    store.add("Unica")

    assert store.complete(5) is None
    assert store.delete(3) is None
    assert [task.text for task in store.tasks] == ["Unica"]


def test_save_and_load_tasks(tmp_path):
    data_file = tmp_path / "tasks.json"

    store = TodoStore(data_path=data_file)
    store.add("Tarea A")
    store.add("Tarea B")
    store.complete(1)

    assert store.save_to_file() is True

    other_store = TodoStore(data_path=data_file)
    assert other_store.load_from_file() is True
    assert [task.text for task in other_store.tasks] == ["Tarea A", "Tarea B"]
    assert [task.completed for task in other_store.tasks] == [False, True]


def test_load_missing_file_is_ok(tmp_path):
    store = TodoStore(data_path=tmp_path / "does_not_exist.json")

    assert store.load_from_file() is True
    assert store.tasks == []


def test_load_invalid_json_returns_false(tmp_path):
    data_file = tmp_path / "bad.json"
    data_file.write_text("{invalid", encoding="utf-8")

    store = TodoStore(data_path=data_file)
    assert store.load_from_file() is False
    assert store.tasks == []


