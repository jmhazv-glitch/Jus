# Ordena una FILA específica de una matriz 3x3 usando Bubble Sort (ascendente)

from typing import List

Matrix = List[List[int]]

def bubble_sort(lista: List[int]) -> List[int]:
    """
    Implementación de Bubble Sort (ascendente) que devuelve una nueva lista.
    """
    arr = lista[:]  # copia para no mutar la original
    n = len(arr)
    for i in range(n - 1):
        intercambiado = False
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                intercambiado = True
        if not intercambiado:  # optimización: si no hubo cambios, ya está ordenada
            break
    return arr

def ordenar_fila_matriz(matriz: Matrix, fila_idx: int) -> Matrix:
    """
    Devuelve una NUEVA matriz donde la fila 'fila_idx' aparece ordenada ascendentemente.
    """
    if fila_idx < 0 or fila_idx >= len(matriz):
        raise IndexError("Índice de fila fuera de rango.")
    nueva = [fila[:] for fila in matriz]          # copia profunda
    nueva[fila_idx] = bubble_sort(nueva[fila_idx])
    return nueva

def main() -> None:
    matriz: Matrix = [
        [8, 3, 5],
        [1, 9, 4],
        [7, 6, 2]
    ]

    print("Matriz ORIGINAL:")
    for fila in matriz:
        print(fila)

    try:
        fila_idx = int(input("\nIngresa el índice de la fila a ordenar (0, 1 o 2): "))
    except ValueError:
        print("Debes ingresar un número entero.")
        return

    try:
        matriz_ordenada = ordenar_fila_matriz(matriz, fila_idx)
    except IndexError as e:
        print(f"Error: {e}")
        return

    print("\nMatriz con la fila ordenada ascendentemente:")
    for fila in matriz_ordenada:
        print(fila)

if __name__ == "__main__":
    main()
