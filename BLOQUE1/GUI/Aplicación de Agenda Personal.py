import re
import tkinter as tk
from datetime import date
import importlib
import json
from pathlib import Path
from tkinter import messagebox, ttk


class AgendaPersonalApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Agenda Personal")
        self.root.geometry("780x460")
        self.root.minsize(680, 420)
        self.ruta_datos = Path(__file__).with_name("agenda_eventos.json")

        self.hora_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.confirmar_eliminacion = tk.BooleanVar(value=True)
        self.gato_imagen = None

        self._construir_interfaz()
        self._cargar_eventos()

    def _construir_interfaz(self) -> None:
        contenedor = ttk.Frame(self.root, padding=12)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        listado_frame = ttk.LabelFrame(contenedor, text="Eventos programados", padding=8)
        listado_frame.grid(row=0, column=0, sticky="nsew")
        listado_frame.columnconfigure(0, weight=1)
        listado_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            listado_frame,
            columns=("fecha", "hora", "descripcion"),
            show="headings",
            height=12,
        )
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripcion")
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("hora", width=100, anchor="center")
        self.tree.column("descripcion", width=470, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(listado_frame, orient="vertical", command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll.set)

        formulario_frame = ttk.LabelFrame(contenedor, text="Nuevo evento", padding=8)
        formulario_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        for col in range(0, 9):
            formulario_frame.columnconfigure(col, weight=0)
        formulario_frame.columnconfigure(7, weight=1)

        ttk.Label(formulario_frame, text="Fecha:").grid(row=0, column=0, sticky="w", padx=(0, 6))

        hoy = date.today()
        try:
            DateEntry = importlib.import_module("tkcalendar").DateEntry

            self.fecha_widget = DateEntry(
                formulario_frame,
                date_pattern="yyyy-mm-dd",
                width=12,
            )
            self.fecha_widget.set_date(hoy)
            self._usar_tkcalendar = True
        except Exception:
            # Fallback sin dependencias extra: selector de fecha con Spinbox.
            self._usar_tkcalendar = False
            self.dia_var = tk.StringVar(value=f"{hoy.day:02d}")
            self.mes_var = tk.StringVar(value=f"{hoy.month:02d}")
            self.anio_var = tk.StringVar(value=str(hoy.year))

            self.fecha_widget = ttk.Frame(formulario_frame)
            tk.Spinbox(
                self.fecha_widget,
                from_=1,
                to=31,
                textvariable=self.dia_var,
                width=3,
                format="%02.0f",
            ).pack(side="left")
            ttk.Label(self.fecha_widget, text="/").pack(side="left", padx=2)
            tk.Spinbox(
                self.fecha_widget,
                from_=1,
                to=12,
                textvariable=self.mes_var,
                width=3,
                format="%02.0f",
            ).pack(side="left")
            ttk.Label(self.fecha_widget, text="/").pack(side="left", padx=2)
            tk.Spinbox(
                self.fecha_widget,
                from_=2000,
                to=2100,
                textvariable=self.anio_var,
                width=5,
            ).pack(side="left")

        self.fecha_widget.grid(row=0, column=1, sticky="w", padx=(0, 14))

        ttk.Label(formulario_frame, text="Hora (HH:MM):").grid(
            row=0, column=2, sticky="w", padx=(0, 6)
        )
        ttk.Entry(formulario_frame, textvariable=self.hora_var, width=10).grid(
            row=0, column=3, sticky="w", padx=(0, 14)
        )

        ttk.Label(formulario_frame, text="Descripcion:").grid(
            row=0, column=4, sticky="w", padx=(0, 6)
        )
        ttk.Entry(formulario_frame, textvariable=self.descripcion_var).grid(
            row=0, column=5, columnspan=3, sticky="ew"
        )

        acciones_frame = ttk.Frame(contenedor, padding=(0, 10, 0, 0))
        acciones_frame.grid(row=2, column=0, sticky="ew")
        acciones_frame.columnconfigure(4, weight=1)

        ttk.Button(acciones_frame, text="Agregar Evento", command=self.agregar_evento).grid(
            row=0, column=0, padx=(0, 8)
        )
        ttk.Button(
            acciones_frame,
            text="Eliminar Evento Seleccionado",
            command=self.eliminar_evento_seleccionado,
        ).grid(row=0, column=1, padx=(0, 8))
        ttk.Checkbutton(
            acciones_frame,
            text="Confirmar eliminacion",
            variable=self.confirmar_eliminacion,
        ).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(acciones_frame, text="Salir", command=self.root.destroy).grid(row=0, column=5)
        self._agregar_decoracion_gato(contenedor)

    def _agregar_decoracion_gato(self, parent: ttk.Frame) -> None:
        candidatos = ["gato.png", "cat.png", "gato.gif"]
        etiqueta_gato = ttk.Label(parent)
        etiqueta_gato.place(relx=1.0, rely=0.0, anchor="ne", x=-6, y=6)

        for nombre in candidatos:
            ruta = Path(__file__).with_name(nombre)
            if not ruta.exists():
                continue

            try:
                self.gato_imagen = tk.PhotoImage(file=str(ruta))
                etiqueta_gato.configure(image=self.gato_imagen)
                return
            except tk.TclError:
                continue

        etiqueta_gato.configure(text="🐱", font=("Segoe UI Emoji", 20))

    def _obtener_fecha(self) -> str:
        if self._usar_tkcalendar:
            return self.fecha_widget.get_date().strftime("%Y-%m-%d")

        fecha_txt = f"{self.dia_var.get().zfill(2)}/{self.mes_var.get().zfill(2)}/{self.anio_var.get()}"
        try:
            dia = int(self.dia_var.get())
            mes = int(self.mes_var.get())
            anio = int(self.anio_var.get())
            date(anio, mes, dia)
        except ValueError:
            raise ValueError("La fecha no es valida.")

        return fecha_txt

    def agregar_evento(self) -> None:
        try:
            fecha = self._obtener_fecha()
        except ValueError as exc:
            messagebox.showerror("Fecha invalida", str(exc))
            return

        hora = self.hora_var.get().strip()
        descripcion = self.descripcion_var.get().strip()

        if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", hora):
            messagebox.showwarning(
                "Hora invalida", "Ingrese una hora con formato HH:MM (24 horas)."
            )
            return

        if not descripcion:
            messagebox.showwarning("Descripcion vacia", "Ingrese una descripcion del evento.")
            return

        self.tree.insert("", "end", values=(fecha, hora, descripcion))
        self.hora_var.set("")
        self.descripcion_var.set("")
        self._guardar_eventos()

    def eliminar_evento_seleccionado(self) -> None:
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin seleccion", "Seleccione un evento para eliminar.")
            return

        if self.confirmar_eliminacion.get():
            confirmar = messagebox.askyesno(
                "Confirmar eliminacion", "Desea eliminar el evento seleccionado?"
            )
            if not confirmar:
                return

        for item in seleccion:
            self.tree.delete(item)

        self._guardar_eventos()

    def _guardar_eventos(self) -> None:
        eventos = []
        for item in self.tree.get_children():
            fecha, hora, descripcion = self.tree.item(item, "values")
            eventos.append(
                {
                    "fecha": fecha,
                    "hora": hora,
                    "descripcion": descripcion,
                }
            )

        try:
            with self.ruta_datos.open("w", encoding="utf-8") as archivo:
                json.dump(eventos, archivo, ensure_ascii=False, indent=2)
        except OSError as exc:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar la agenda en {self.ruta_datos.name}.\n{exc}",
            )

    def _cargar_eventos(self) -> None:
        if not self.ruta_datos.exists():
            return

        try:
            with self.ruta_datos.open("r", encoding="utf-8") as archivo:
                eventos = json.load(archivo)
        except json.JSONDecodeError:
            messagebox.showwarning(
                "Archivo invalido",
                f"{self.ruta_datos.name} esta corrupto o no tiene formato JSON valido.",
            )
            return
        except OSError as exc:
            messagebox.showerror(
                "Error al cargar",
                f"No se pudo leer {self.ruta_datos.name}.\n{exc}",
            )
            return

        if not isinstance(eventos, list):
            messagebox.showwarning(
                "Formato invalido",
                f"{self.ruta_datos.name} no contiene una lista de eventos.",
            )
            return

        for evento in eventos:
            if not isinstance(evento, dict):
                continue

            fecha = str(evento.get("fecha", "")).strip()
            hora = str(evento.get("hora", "")).strip()
            descripcion = str(evento.get("descripcion", "")).strip()

            if fecha and hora and descripcion:
                self.tree.insert("", "end", values=(fecha, hora, descripcion))


def main() -> None:
    root = tk.Tk()
    AgendaPersonalApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
