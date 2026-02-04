import threading
import time
from typing import List

# Función que simula una tarea para un hilo
def tarea_hilo(identificador: int, delay: float, iteraciones: int = 5) -> None:
    """
    Ejecuta una tarea en un hilo separado.

    Args:
        identificador: ID único del hilo
        delay: Tiempo de espera en segundos entre iteraciones
        iteraciones: Número de iteraciones (por defecto 5)
    """
    for i in range(iteraciones):
        print(f'Hilo {identificador}: Realizando tarea {i}')
        time.sleep(delay)
    print(f'Hilo {identificador}: Completado')

def crear_y_ejecutar_hilos(hilos_config: List[tuple]) -> None:
    """
    Crea y ejecuta múltiples hilos de forma escalable.

    Args:
        hilos_config: Lista de tuplas (identificador, delay)
    """
    hilos = []

    # Crear y iniciar hilos
    for identificador, delay in hilos_config:
        hilo = threading.Thread(
            target=tarea_hilo,
            args=(identificador, delay),
            daemon=False  # Permite control explícito del ciclo de vida
        )
        hilos.append(hilo)
        hilo.start()

    # Esperar a que todos los hilos terminen
    for hilo in hilos:
        hilo.join()

    print('Programa principal: Todas las tareas han sido completadas.')

if __name__ == '__main__':
    # Configuración de hilos: (identificador, delay)
    configuracion = [
        (1, 1.0),
        (2, 0.8),
        (3, 1.2)
    ]

    crear_y_ejecutar_hilos(configuracion)

