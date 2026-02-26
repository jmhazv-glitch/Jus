"""
Módulo main.py
"""
from producto import Producto
from inventario import Inventario
import os

def limpiar_pantalla():

    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():

    gato = [
        r"   /\_____/\   ",
        r"  /  o   o  \  ",
        r" ( ==  ^  == ) ",
        r"  )         (  ",
        r" (           ) ",
        r"( (  )   (  ) )",
        r"(__(__)___(__)_)",
    ]

    menu = [
        "╔═══════════════════════════════════════════════╗",
        "║   SISTEMA AVANZADO DE GESTIÓN DE INVENTARIO   ║",
        "╠═══════════════════════════════════════════════╣",
        "║   1. Añadir nuevo producto                    ║",
        "║   2. Eliminar producto                        ║",
        "║   3. Actualizar cantidad de producto          ║",
        "║   4. Actualizar precio de producto            ║",
        "║   5. Buscar producto por nombre               ║",
        "║   6. Buscar producto por ID                   ║",
        "║   7. Mostrar todos los productos              ║",
        "║   8. Mostrar estadísticas del inventario      ║",
        "║   9. Salir                                    ║",
        "╚═══════════════════════════════════════════════╝",
    ]

    ancho_gato = max(len(linea) for linea in gato)
    inicio_gato = (len(menu) - len(gato)) // 2

    print()
    for i, linea_menu in enumerate(menu):
        idx_gato = i - inicio_gato
        if 0 <= idx_gato < len(gato):
            print(f"{linea_menu}  {gato[idx_gato]}")
        else:
            print(linea_menu)

def validar_entero(mensaje: str) -> int:
    """Valida que la entrada del usuario sea un número entero."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print(" Error: Por favor ingrese un número entero válido.")


def validar_float(mensaje: str) -> float:
    """Valida que la entrada del usuario sea un número decimal positivo."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print(" Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print(" Error: Por favor ingrese un número válido.")


def agregar_producto(inventario: Inventario):
    """Flujo para agregar un nuevo producto."""
    print("\n--- AÑADIR NUEVO PRODUCTO ---")

    id_sugerido = inventario.siguiente_id()
    print(f"   (ID sugerido: {id_sugerido})")

    id_prod = validar_entero("Ingrese el ID del producto: ")
    nombre = input("Ingrese el nombre del producto: ").strip()

    if not nombre:
        print(" Error: El nombre no puede estar vacío.")
        return

    if '|' in nombre:
        print(" Error: El nombre no puede contener el carácter '|'.")
        return

    cantidad = validar_entero("Ingrese la cantidad: ")
    if cantidad < 0:
        print(" Error: La cantidad no puede ser negativa.")
        return

    precio = validar_float("Ingrese el precio: $")

    nuevo_producto = Producto(id_prod, nombre, cantidad, precio)
    exito, mensaje = inventario.agregar_producto(nuevo_producto)
    print(mensaje)


def eliminar_producto(inventario: Inventario):
    """Flujo para eliminar un producto."""
    print("\n--- ELIMINAR PRODUCTO ---")

    id_prod = validar_entero("Ingrese el ID del producto a eliminar: ")

    producto = inventario.buscar_por_id(id_prod)
    if producto:
        print(f"\nProducto encontrado: {producto}")
        confirmacion = input("¿Está seguro de eliminar este producto? (s/n): ").lower()
        if confirmacion == 's':
            exito, mensaje = inventario.eliminar_producto(id_prod)
            print(mensaje)
        else:
            print("Operación cancelada.")
    else:
        print(f" Error: No se encontró un producto con el ID {id_prod}.")


def actualizar_cantidad(inventario: Inventario):
    """Flujo para actualizar la cantidad de un producto."""
    print("\n--- ACTUALIZAR CANTIDAD DE PRODUCTO ---")

    id_prod = validar_entero("Ingrese el ID del producto: ")

    producto = inventario.buscar_por_id(id_prod)
    if producto:
        print(f"\nProducto actual: {producto}")
        nueva_cantidad = validar_entero(f"Ingrese la nueva cantidad (actual: {producto.get_cantidad()}): ")

        if nueva_cantidad < 0:
            print(" Error: La cantidad no puede ser negativa.")
            return

        exito, mensaje = inventario.actualizar_cantidad(id_prod, nueva_cantidad)
        print(mensaje)
        if exito:
            print(f"Nueva información: {producto}")
    else:
        print(f" Error: No se encontró un producto con el ID {id_prod}.")


def actualizar_precio(inventario: Inventario):
    """Flujo para actualizar el precio de un producto."""
    print("\n--- ACTUALIZAR PRECIO DE PRODUCTO ---")

    id_prod = validar_entero("Ingrese el ID del producto: ")

    producto = inventario.buscar_por_id(id_prod)
    if producto:
        print(f"\nProducto actual: {producto}")
        nuevo_precio = validar_float(f"Ingrese el nuevo precio (actual: ${producto.get_precio():.2f}): $")

        exito, mensaje = inventario.actualizar_precio(id_prod, nuevo_precio)
        print(mensaje)
        if exito:
            print(f"Nueva información: {producto}")
    else:
        print(f" Error: No se encontró un producto con el ID {id_prod}.")


def buscar_por_nombre(inventario: Inventario):
    """Flujo para buscar productos por nombre."""
    print("\n--- BUSCAR PRODUCTO POR NOMBRE ---")

    nombre = input("Ingrese el nombre o parte del nombre a buscar: ").strip()

    if not nombre:
        print(" Error: Debe ingresar un nombre para buscar.")
        return

    resultados = inventario.buscar_por_nombre(nombre)
    if resultados:
        print(f"\n🔍 Se encontraron {len(resultados)} producto(s):")
        print("-" * 65)
        for producto in resultados:
            print(f"   {producto}")
        print("-" * 65)
    else:
        print(f" No se encontraron productos con el nombre '{nombre}'.")


def buscar_por_id(inventario: Inventario):
    """Flujo para buscar un producto por ID."""
    print("\n--- BUSCAR PRODUCTO POR ID ---")

    id_prod = validar_entero("Ingrese el ID del producto: ")

    producto = inventario.buscar_por_id(id_prod)
    if producto:
        print(f"\n🔍 Producto encontrado:")
        print("-" * 65)
        print(f"   {producto}")
        print("-" * 65)
    else:
        print(f" No se encontró un producto con el ID {id_prod}.")


def main():
    """Punto de entrada principal del programa."""
    inventario = Inventario()

    # Diccionario de acciones del menú (colección para mapear opciones)
    acciones: dict = {
        1: agregar_producto,
        2: eliminar_producto,
        3: actualizar_cantidad,
        4: actualizar_precio,
        5: buscar_por_nombre,
        6: buscar_por_id,
        7: lambda inv: inv.mostrar_todos(),
        8: lambda inv: inv.mostrar_estadisticas(),
    }

    while True:
        mostrar_menu()
        opcion = validar_entero("   Seleccione una opción: ")

        if opcion == 9:
            print("\n ¡Hasta luego! Inventario guardado correctamente.")
            break

        accion = acciones.get(opcion)
        if accion:
            accion(inventario)
        else:
            print("\n  Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()

