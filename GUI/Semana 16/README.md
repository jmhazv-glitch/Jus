# Semana 16 - Aplicacion GUI de Tareas Pendientes

Aplicacion de escritorio hecha con Tkinter para gestionar una lista de tareas.

## Funcionalidades

- Agregar tareas con boton **Anadir** o tecla **Enter**.
- Marcar tarea como completada con boton **Completar** o tecla **C**.
- Eliminar tarea con boton **Eliminar** o tecla **Delete**/**D**.
- Cerrar la aplicacion con tecla **Escape**.
- Feedback visual en la lista:
  - `"[ ]"` para pendientes
  - `"[x]"` y color gris para completadas
- Persistencia automatica en `todo_tasks.json` (se carga al abrir y se guarda al cambiar tareas).

## Estructura

- `todo_app.py`: interfaz Tkinter + logica de tareas.
- `tests/test_todo_app.py`: pruebas unitarias de la logica base.
- `requirements.txt`: dependencias para ejecutar pruebas.

## Ejecucion

```bash
python3 "todo_app.py"
```

## Ejecutar pruebas

```bash
python3 -m pytest "tests/test_todo_app.py" -q
```

