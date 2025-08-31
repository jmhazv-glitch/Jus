# Búsqueda lineal en una matriz 3x3 (sin librerías externas)

from typing import List, Tuple, Optional

Matrix = List[List[int]]

def buscar_en_matriz(matriz: Matrix, objetivo: int) -> Optional[Tuple[int, int]]:
    """
    Recorre la matriz y devuelve la posición (fila, columna) del primer
    elemento que coincide con 'objetivo'. Si no existe, devuelve None.
    """
    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            if valor == objetivo:
                return i, j
    return None

def main() -> None:
    matriz: Matrix = [
        [8, 3, 5],
        [1, 9, 4],
        [7, 6, 2]
    ]

    print("Matriz 3x3:")
    for fila in matriz:
        print(fila)

    try:
        objetivo = int(input("\nIngresa el valor a buscar: "))
    except ValueError:
        print("Debes ingresar un número entero.")
        return

    pos = buscar_en_matriz(matriz, objetivo)
    if pos is None:
        print(f"❌ El valor {objetivo} NO se encuentra en la matriz.")
    else:
        i, j = pos
        print(f"✅ Encontrado: {objetivo} en posición (fila={i}, columna={j}).")

if __name__ == "__main__":
    main()
