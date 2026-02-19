"""
Módulo main.py
Sistema de Gestión de Inventarios - Interfaz de Usuario
Proporciona un menú interactivo en consola para gestionar el inventario.
"""

from producto import Producto
from inventario import Inventario
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n" + "="*60)
    print(" SISTEMA DE GESTION DE INVENTARIOS ".center(60))
    print("="*60)
    print("\n1. Añadir nuevo producto")
    print("2. Eliminar producto")
    print("3. Actualizar cantidad de producto")
    print("4. Actualizar precio de producto")
    print("5. Buscar producto por nombre")
    print("6. Buscar producto por ID")
    print("7. Mostrar todos los productos")
    print("8. Mostrar estadísticas del inventario")
    print("9. Salir")
    print("\n" + "="*60)

def validar_entero(mensaje):
    """
    Valida que la entrada del usuario sea un número entero.

    Args:
        mensaje (str): Mensaje a mostrar al usuario
        
    Returns:
        int: Número entero válido ingresado por el usuario
    """
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("❌ Error: Por favor ingrese un número entero válido.")

def validar_float(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("❌ Error: El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("❌ Error: Por favor ingrese un número válido.")

def agregar_producto(inventario):
    print("\n--- AÑADIR NUEVO PRODUCTO ---")

    id = validar_entero("Ingrese el ID del producto: ")
    nombre = input("Ingrese el nombre del producto: ").strip()
    
    if not nombre:
        print("❌ Error: El nombre no puede estar vacío.")
        return

    if '|' in nombre:
        print("❌ Error: El nombre no puede contener el carácter '|'.")
        return

    cantidad = validar_entero("Ingrese la cantidad: ")
    if cantidad < 0:
        print("❌ Error: La cantidad no puede ser negativa.")
        return
    
    precio = validar_float("Ingrese el precio: $")


    nuevo_producto = Producto(id, nombre, cantidad, precio)
    

    exito, mensaje = inventario.agregar_producto(nuevo_producto)
    print(mensaje)

def eliminar_producto(inventario):



    print("\n--- ELIMINAR PRODUCTO ---")
    
    id = validar_entero("Ingrese el ID del producto a eliminar: ")
    
    # Primero buscar el producto para mostrar información
    producto = inventario.buscar_por_id(id)
    if producto:
        print(f"\nProducto encontrado: {producto}")
        confirmacion = input("¿Está seguro de eliminar este producto? (s/n): ").lower()

        if confirmacion == 's':
            # El método ahora retorna una tupla (exito, mensaje)
            exito, mensaje = inventario.eliminar_producto(id)
            print(mensaje)
        else:
            print("Operación cancelada.")
    else:
        print(f"❌ Error: No se encontró un producto con el ID {id}.")

def actualizar_cantidad(inventario):
    """
    Función para actualizar la cantidad de un producto.
    Notifica al usuario sobre el éxito o fallo de la operación de archivo.

    Args:
        inventario (Inventario): Objeto inventario donde se actualizará el producto
    """
    print("\n--- ACTUALIZAR CANTIDAD DE PRODUCTO ---")
    
    id = validar_entero("Ingrese el ID del producto: ")
    
    # Mostrar información actual del producto
    producto = inventario.buscar_por_id(id)
    if producto:
        print(f"\nProducto actual: {producto}")
        nueva_cantidad = validar_entero(f"Ingrese la nueva cantidad (actual: {producto.get_cantidad()}): ")
        
        if nueva_cantidad < 0:
            print("❌ Error: La cantidad no puede ser negativa.")
            return
        
        # El método ahora retorna una tupla (exito, mensaje)
        exito, mensaje = inventario.actualizar_cantidad(id, nueva_cantidad)
        print(mensaje)
        if exito:
            print(f"Nueva información: {producto}")
    else:
        print(f"❌ Error: No se encontró un producto con el ID {id}.")

def actualizar_precio(inventario):
    """
    Función para actualizar el precio de un producto.
    Notifica al usuario sobre el éxito o fallo de la operación de archivo.

    Args:
        inventario (Inventario): Objeto inventario donde se actualizará el producto
    """
    print("\n--- ACTUALIZAR PRECIO DE PRODUCTO ---")
    
    id = validar_entero("Ingrese el ID del producto: ")
    
    # Mostrar información actual del producto
    producto = inventario.buscar_por_id(id)
    if producto:
        print(f"\nProducto actual: {producto}")
        nuevo_precio = validar_float(f"Ingrese el nuevo precio (actual: ${producto.get_precio():.2f}): $")
        
        # El método ahora retorna una tupla (exito, mensaje)
        exito, mensaje = inventario.actualizar_precio(id, nuevo_precio)
        print(mensaje)
        if exito:
            print(f"Nueva información: {producto}")
    else:
        print(f"❌ Error: No se encontró un producto con el ID {id}.")

def buscar_por_nombre(inventario):
    """
    Función para buscar productos por nombre.

    Args:
        inventario (Inventario): Objeto inventario donde se buscarán los productos
    """
    print("\n--- BUSCAR PRODUCTO POR NOMBRE ---")
    
    nombre = input("Ingrese el nombre o parte del nombre a buscar: ").strip()
    
    if not nombre:
        print("Error: Debe ingresar un nombre para buscar.")
        return
    
    resultados = inventario.buscar_por_nombre(nombre)
    
    if resultados:
        print(f"\n Se encontraron {len(resultados)} producto(s):")
        print("-" * 80)
        for producto in resultados:
            print(producto)
        print("-" * 80)
    else:
        print(f"❌ No se encontraron productos con el nombre '{nombre}'.")

def buscar_por_id(inventario):
    """
    Función para buscar un producto por ID.

    Args:
        inventario (Inventario): Objeto inventario donde se buscará el producto
    """
    print("\n--- BUSCAR PRODUCTO POR ID ---")
    
    id = validar_entero("Ingrese el ID del producto: ")
    
    producto = inventario.buscar_por_id(id)
    
    if producto:
        print("\n📦 Producto encontrado:")
        print("-" * 80)
        print(producto)
        print("-" * 80)
    else:
        print(f"❌ No se encontró un producto con el ID {id}.")

def mostrar_todos_productos(inventario):
    """
    Función para mostrar todos los productos en el inventario.

    Args:
        inventario (Inventario): Objeto inventario a mostrar
    """
    print("\n--- TODOS LOS PRODUCTOS ---")
    
    productos = inventario.mostrar_todos()
    
    if productos:
        print(f"\n Total de productos en inventario: {len(productos)}")
        print("-" * 80)
        for producto in productos:
            print(producto)
        print("-" * 80)
    else:
        print("❌ El inventario está vacío.")

def mostrar_estadisticas(inventario):
    """
    Función para mostrar estadísticas del inventario.

    Args:
        inventario (Inventario): Objeto inventario a analizar
    """
    print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")

    total_productos = inventario.obtener_total_productos()
    valor_total = inventario.obtener_valor_total_inventario()
    
    if total_productos > 0:
        productos = inventario.mostrar_todos()
        total_unidades = sum(p.get_cantidad() for p in productos)
        
        print(f"\n📊 Resumen del Inventario:")
        print("-" * 60)
        print(f"  • Tipos de productos diferentes: {total_productos}")
        print(f"  • Total de unidades en stock: {total_unidades}")
        print(f"  • Valor total del inventario: ${valor_total:.2f}")
        print(f"  • Valor promedio por producto: ${valor_total/total_productos:.2f}")
        print("-" * 60)
        
        # Producto más caro y más barato
        producto_mas_caro = max(productos, key=lambda p: p.get_precio())
        producto_mas_barato = min(productos, key=lambda p: p.get_precio())
        
        print(f"\n   Producto más caro:")
        print(f"     {producto_mas_caro}")
        print(f"\n   Producto más barato:")
        print(f"     {producto_mas_barato}")
        print("-" * 60)
    else:
        print("❌ El inventario está vacío. No hay estadísticas para mostrar.")

def main():
    """
    Función principal que ejecuta el sistema de gestión de inventarios.
    Al iniciar, carga automáticamente los productos desde el archivo de inventario.
    """
    print("\n" + "="*60)
    print(" INICIANDO SISTEMA DE GESTIÓN DE INVENTARIOS ".center(60))
    print("="*60)

    # Crear instancia del inventario
    # El constructor carga automáticamente los productos desde el archivo si existe
    inventario = Inventario()
    
    # Mostrar información sobre la carga del archivo
    print(f"\nArchivo de inventario: {inventario.get_ruta_archivo()}")

    # Verificar si hay error en la carga
    if inventario.get_ultimo_error():
        print(inventario.get_ultimo_error())
    else:
        total_productos = inventario.obtener_total_productos()
        if total_productos > 0:
            print(f"Se cargaron {total_productos} productos desde el archivo.")
        else:
            print(" No se encontraron productos previos. El inventario está vacío.")
            print("\n¿Desea cargar productos de ejemplo para pruebas? (s/n): ", end="")
            respuesta = input().strip().lower()
            if respuesta == 's':
                # Agregar productos de ejemplo
                print("\nCargando productos de ejemplo...")
                productos_ejemplo = [
                    Producto(1, "Laptop HP", 10, 899.99),
                    Producto(2, "Mouse Logitech", 50, 25.50),
                    Producto(3, "Teclado Mecánico", 30, 75.00),
                    Producto(4, "Monitor Samsung 24\"", 15, 199.99),
                    Producto(5, "Webcam HD", 20, 45.00)
                ]
                for producto in productos_ejemplo:
                    exito, mensaje = inventario.agregar_producto(producto)
                    if not exito:
                        print(f"   No se pudo agregar: {producto.get_nombre()}")
                print("Productos de ejemplo cargados exitosamente.")

    # Bucle principal del programa
    while True:
        mostrar_menu()
        
        opcion = input("\nSeleccione una opción (1-9): ").strip()

        if opcion == '1':
            agregar_producto(inventario)
        elif opcion == '2':
            eliminar_producto(inventario)
        elif opcion == '3':
            actualizar_cantidad(inventario)
        elif opcion == '4':
            actualizar_precio(inventario)
        elif opcion == '5':
            buscar_por_nombre(inventario)
        elif opcion == '6':
            buscar_por_id(inventario)
        elif opcion == '7':
            mostrar_todos_productos(inventario)
        elif opcion == '8':
            mostrar_estadisticas(inventario)
        elif opcion == '9':
            print("\n" + "="*60)
            print(" ¡Gracias por usar el Sistema de Gestión de Inventarios! ".center(60))
            print(f" Los datos han sido guardados en: {inventario.get_ruta_archivo()} ".center(60))
            print("="*60 + "\n")
            break
        else:
            print("❌ Opción inválida. Por favor seleccione una opción del 1 al 9.")

        input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    main()
