import random
import time

class Memoria:
    def __init__(self, tamanio):
        self.tamanio = tamanio
        self.memoria = [None] * tamanio

    def asignar(self, proceso, tamanio_requerido):
        for i in range(self.tamanio - tamanio_requerido + 1):
            if all(self.memoria[i + j] is None for j in range(tamanio_requerido)):
                for j in range(tamanio_requerido):
                    self.memoria[i + j] = proceso
                print(f'Proceso {proceso} asigno {tamanio_requerido} bloques de memoria.')
                return True
        print(f'Proceso {proceso} no pudo asignar memoria.')
        return False

    def liberar(self, proceso):
        for i in range(self.tamanio):
            if self.memoria[i] == proceso:
                self.memoria[i] = None
        print(f'Proceso {proceso} ha liberado su memoria.')

    def mostrar_memoria(self):
        print('Estado actual de la memoria:')
        print(self.memoria)

def proceso(nombre, memoria):
    tamanio_requerido = random.randint(1, 5)
    print(f'{nombre} esta pidiendo {tamanio_requerido} bloques de memoria.')
    if memoria.asignar(nombre, tamanio_requerido):
        time.sleep(random.randint(1, 3))
        memoria.liberar(nombre)
    time.sleep(random.randint(1, 2))

def gestionar_memoria():
    memoria = Memoria(10)
    procesos = ['Proceso-A', 'Proceso-B', 'Proceso-C', 'Proceso-D', 'Proceso-E']
    for i in range(5):
        proceso_nombre = random.choice(procesos)
        proceso(proceso_nombre, memoria)
    memoria.mostrar_memoria()

if __name__ == '__main__':
    gestionar_memoria()