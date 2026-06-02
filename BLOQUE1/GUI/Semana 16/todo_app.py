import json
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import ttk


@dataclass
class TodoItem:
    text: str
    completed: bool = False


class TodoStore:
    """In-memory task storage with basic validation."""

    def __init__(self, data_path: Path | None = None) -> None:
        self._tasks: list[TodoItem] = []
        self.data_path = data_path or Path(__file__).with_name("todo_tasks.json")

    def add(self, raw_text: str | None) -> TodoItem | None:
        text = (raw_text or "").strip()
        if not text:
            return None
        item = TodoItem(text=text)
        self._tasks.append(item)
        return item

    def complete(self, index: int) -> TodoItem | None:
        if 0 <= index < len(self._tasks):
            self._tasks[index].completed = True
            return self._tasks[index]
        return None

    def delete(self, index: int) -> TodoItem | None:
        if 0 <= index < len(self._tasks):
            return self._tasks.pop(index)
        return None

    @property
    def tasks(self) -> list[TodoItem]:
        return [TodoItem(task.text, task.completed) for task in self._tasks]

    def save_to_file(self, path: Path | None = None) -> bool:
        target = path or self.data_path
        payload = [{"text": task.text, "completed": task.completed} for task in self._tasks]
        try:
            target.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            return True
        except OSError:
            return False

    def load_from_file(self, path: Path | None = None) -> bool:
        target = path or self.data_path
        if not target.exists():
            return True

        try:
            raw_data = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False

        if not isinstance(raw_data, list):
            return False

        loaded: list[TodoItem] = []
        for item in raw_data:
            if not isinstance(item, dict):
                continue

            text = str(item.get("text", "")).strip()
            if not text:
                continue

            loaded.append(TodoItem(text=text, completed=bool(item.get("completed", False))))

        self._tasks = loaded
        return True


class TodoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Lista de tareas pendientes")
        self.root.minsize(520, 340)

        self.store = TodoStore()
        self.status = tk.StringVar(value="Escribe una tarea y presiona Enter")

        if not self.store.load_from_file():
            self.status.set("No se pudo cargar el archivo de tareas")

        self._build_ui()
        self._bind_shortcuts()
        self.render_tasks()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.grid(column=0, row=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)

        ttk.Label(container, text="Nueva tarea:").grid(column=0, row=0, sticky="w")

        self.entry = ttk.Entry(container)
        self.entry.grid(column=0, row=1, sticky="ew", pady=(4, 10))
        self.entry.focus_set()

        controls = ttk.Frame(container)
        controls.grid(column=1, row=1, sticky="n", padx=(8, 0))

        self.add_button = ttk.Button(controls, text="Anadir", command=self.on_add)
        self.add_button.grid(column=0, row=0, sticky="ew")

        self.complete_button = ttk.Button(controls, text="Completar", command=self.on_complete)
        self.complete_button.grid(column=0, row=1, sticky="ew", pady=4)

        self.delete_button = ttk.Button(controls, text="Eliminar", command=self.on_delete)
        self.delete_button.grid(column=0, row=2, sticky="ew")

        self.listbox = tk.Listbox(container, activestyle="none", selectmode=tk.SINGLE)
        self.listbox.grid(column=0, row=2, columnspan=2, sticky="nsew")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(column=1, row=2, sticky="nse")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        ttk.Label(container, textvariable=self.status).grid(column=0, row=3, columnspan=2, sticky="w", pady=(10, 0))

    def _bind_shortcuts(self) -> None:
        self.entry.bind("<Return>", self.on_add)

        self.listbox.bind("<Double-Button-1>", self.on_complete)
        self.listbox.bind("<Delete>", self.on_delete)
        self.listbox.bind("<Key-d>", self.on_delete)
        self.listbox.bind("<Key-D>", self.on_delete)
        self.listbox.bind("<Key-c>", self.on_complete)
        self.listbox.bind("<Key-C>", self.on_complete)

        self.root.bind("<Delete>", self.on_delete)
        self.root.bind("<Key-d>", self.on_delete)
        self.root.bind("<Key-D>", self.on_delete)
        self.root.bind("<Key-c>", self.on_complete)
        self.root.bind("<Key-C>", self.on_complete)
        self.root.bind("<Escape>", self.on_close)

    @property
    def selected_index(self) -> int | None:
        selection = self.listbox.curselection()
        if not selection:
            return None
        return int(selection[0])

    def on_add(self, event: tk.Event | None = None) -> str:
        del event
        item = self.store.add(self.entry.get())
        if item is None:
            self.status.set("No puedes agregar una tarea vacia")
            return "break"

        self.entry.delete(0, tk.END)
        self.render_tasks(selected=self.listbox.size())
        if self.store.save_to_file():
            self.status.set(f"Tarea agregada: {item.text}")
        else:
            self.status.set("Tarea agregada, pero no se pudo guardar el archivo")
        return "break"

    def on_complete(self, event: tk.Event | None = None) -> str:
        del event
        index = self.selected_index
        if index is None:
            self.status.set("Selecciona una tarea para marcarla")
            return "break"

        item = self.store.complete(index)
        if item is None:
            self.status.set("No se pudo completar la tarea seleccionada")
            return "break"

        self.render_tasks(selected=index)
        if self.store.save_to_file():
            self.status.set(f"Tarea completada: {item.text}")
        else:
            self.status.set("Tarea completada, pero no se pudo guardar el archivo")
        return "break"

    def on_delete(self, event: tk.Event | None = None) -> str:
        del event
        index = self.selected_index
        if index is None:
            self.status.set("Selecciona una tarea para eliminarla")
            return "break"

        item = self.store.delete(index)
        if item is None:
            self.status.set("No se pudo eliminar la tarea seleccionada")
            return "break"

        self.render_tasks(selected=max(0, index - 1))
        if self.store.save_to_file():
            self.status.set(f"Tarea eliminada: {item.text}")
        else:
            self.status.set("Tarea eliminada, pero no se pudo guardar el archivo")
        return "break"

    def on_close(self, event: tk.Event | None = None) -> str:
        del event
        self.store.save_to_file()
        self.root.destroy()
        return "break"

    def render_tasks(self, selected: int | None = None) -> None:
        self.listbox.delete(0, tk.END)
        tasks = self.store.tasks
        for task in tasks:
            prefix = "[x]" if task.completed else "[ ]"
            self.listbox.insert(tk.END, f"{prefix} {task.text}")

        for idx, task in enumerate(tasks):
            if task.completed:
                try:
                    self.listbox.itemconfig(idx, fg="#6b7280")
                except tk.TclError:
                    # Some Tk builds may not support per-item colors.
                    pass

        if selected is not None and self.listbox.size() > 0:
            safe_index = min(selected, self.listbox.size() - 1)
            self.listbox.selection_set(safe_index)
            self.listbox.activate(safe_index)
            self.listbox.see(safe_index)


def main() -> None:
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

