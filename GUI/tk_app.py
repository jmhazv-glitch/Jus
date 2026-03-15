import tkinter as tk
from tkinter import ttk


class ItemStore:
    """Simple in-memory store for strings with trim/empty validation."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def add(self, raw_text: str | None) -> str | None:
        value = (raw_text or "").strip()
        if not value:
            return None
        self._items.append(value)
        return value

    def clear(self) -> None:
        self._items.clear()

    @property
    def items(self) -> list[str]:
        return list(self._items)


class InfoApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Bloc de notas sencillo")

        self.store = ItemStore()
        self.status = tk.StringVar(value="Listo para agregar notas")

        container = ttk.Frame(self.root, padding=12)
        container.grid(column=0, row=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Gatito decorativo
        ttk.Label(container, text="🐱", font=("TkDefaultFont", 28)).grid(
            column=2, row=0, sticky="e", pady=(0, 4)
        )

        # Entrada y acciones
        ttk.Label(container, text="Ingresa un texto y presiona Agregar:").grid(
            column=0, row=0, columnspan=2, sticky="w"
        )

        self.entry = ttk.Entry(container, width=40)
        self.entry.grid(column=0, row=1, columnspan=2, sticky="ew", padx=(0, 8), pady=(6, 6))
        self.entry.focus_set()
        container.columnconfigure(0, weight=1)

        self.add_button = ttk.Button(container, text="Agregar", command=self.on_add)
        self.add_button.grid(column=2, row=1, sticky="ew")

        self.clear_button = ttk.Button(container, text="Limpiar", command=self.on_clear)
        self.clear_button.grid(column=2, row=2, sticky="ew", pady=(0, 6))

        # Lista de datos
        columns = ("texto",)
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=10)
        self.tree.heading("texto", text="Texto ingresado")
        self.tree.grid(column=0, row=2, columnspan=2, sticky="nsew", pady=(0, 6))
        container.rowconfigure(2, weight=1)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        scrollbar.grid(column=1, row=2, sticky="nse")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Estado
        ttk.Label(container, textvariable=self.status).grid(column=0, row=3, columnspan=3, sticky="w")

        # Enlaces de eventos
        self.entry.bind("<Return>", self.on_add)
        self.entry.bind("<KeyRelease>", self.update_add_state)
        self.root.bind("<Escape>", self.on_clear)

        self.update_add_state()

    def on_add(self, event: tk.Event | None = None) -> None:
        del event  # Event not used directly
        value = self.store.add(self.entry.get())
        if value is None:
            self.status.set("Escribe algo antes de agregar")
            self.update_add_state()
            return

        self.tree.insert("", tk.END, values=(value,))
        self.entry.delete(0, tk.END)
        self.status.set(f"Agregado: {value}")
        self.update_add_state()

    def on_clear(self, event: tk.Event | None = None) -> None:
        del event
        if not self.store.items:
            self.status.set("No hay nada para limpiar")
            return

        self.store.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.entry.delete(0, tk.END)
        self.status.set("Lista limpia")
        self.update_add_state()
        self.entry.focus_set()

    def update_add_state(self, event: tk.Event | None = None) -> None:
        del event
        text = self.entry.get().strip()
        if text:
            self.add_button.state(["!disabled"])
        else:
            self.add_button.state(["disabled"])


def main() -> None:
    root = tk.Tk()
    app = InfoApp(root)
    # Mantiene el redimensionado amigable
    root.minsize(400, 300)
    root.mainloop()


if __name__ == "__main__":
    main()

