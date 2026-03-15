import pytest

try:
    from GUI.tk_app import ItemStore
except ImportError as exc:  # tkinter might be missing in headless envs
    pytest.skip(f"tk_app import skipped: {exc}", allow_module_level=True)


def test_add_trims_and_stores():
    store = ItemStore()
    added = store.add("  hola  ")
    assert added == "hola"
    assert store.items == ["hola"]


def test_add_rejects_empty_strings():
    store = ItemStore()
    assert store.add("   ") is None
    assert store.items == []


def test_clear_removes_all_items():
    store = ItemStore()
    store.add("uno")
    store.add("dos")
    store.clear()
    assert store.items == []

