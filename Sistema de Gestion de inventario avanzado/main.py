"""
Sistema Avanzado de Gestión de Inventario
==========================================
Desarrollado con POO, colecciones y almacenamiento en archivos.
"""

import json
import os


# ──────────────────────────────────────────────
# Clase Producto
# ──────────────────────────────────────────────
class Producto:
    """Representa un producto del inventario."""

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # ── Getters ──
    def get_id(self) -> int:
        return self.__id

    def get_nombre(self) -> str:
        return self.__nombre

    def get_cantidad(self) -> int:
        return self.__cantidad

    def get_precio(self) -> float:
        return self.__precio

    # ── Setters ──
    def set_nombre(self, nombre: str):
        self.__nombre = nombre

    def set_cantidad(self, cantidad: int):
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad

    def set_precio(self, precio: float):
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio

    # ── Representación ──
    def __str__(self) -> str:
        return (f"ID: {self.__id} | Nombre: {self.__nombre} | "
                f"Cantidad: {self.__cantidad} | Precio: ${self.__precio:,.2f}")

    def to_dict(self) -> dict:
        """Serializa el producto a diccionario para almacenamiento."""
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        """Deserializa un diccionario a un objeto Producto."""
        return cls(datos["id"], datos["nombre"], datos["cantidad"], datos["precio"])


# ──────────────────────────────────────────────
# Clase Inventario
# ──────────────────────────────────────────────
class Inventario:
    """Gestiona la colección de productos del inventario."""

    ARCHIVO = "inventario.json"

    def __init__(self):
        # Diccionario {id: Producto} → búsqueda rápida O(1)
        self.__productos: dict[int, Producto] = {}
        # Conjunto de IDs para validar unicidad rápidamente
        self.__ids: set[int] = set()
        # Índice invertido nombre→set(ids) para búsqueda por nombre
        self.__indice_nombre: dict[str, set[int]] = {}
        # Cargar datos persistentes al iniciar
        self.cargar_desde_archivo()

    # ── Propiedades de consulta ──
    @property
    def total_productos(self) -> int:
        return len(self.__productos)

    # ── Métodos principales ──
    def agregar_producto(self, producto: Producto) -> bool:
        """Añade un nuevo producto al inventario."""
        if producto.get_id() in self.__ids:
            print(f"\n⚠️  Ya existe un producto con ID {producto.get_id()}.")
            return False
        self.__productos[producto.get_id()] = producto
        self.__ids.add(producto.get_id())
        self.__actualizar_indice_nombre(producto, agregar=True)
        self.guardar_en_archivo()
        print(f"\n✅ Producto '{producto.get_nombre()}' agregado exitosamente.")
        return True

    def eliminar_producto(self, id_producto: int) -> bool:
        """Elimina un producto por su ID."""
        if id_producto not in self.__ids:
            print(f"\n⚠️  No se encontró un producto con ID {id_producto}.")
            return False
        producto = self.__productos[id_producto]
        self.__actualizar_indice_nombre(producto, agregar=False)
        del self.__productos[id_producto]
        self.__ids.discard(id_producto)
        self.guardar_en_archivo()
        print(f"\n🗑️  Producto '{producto.get_nombre()}' eliminado correctamente.")
        return True

    def actualizar_producto(self, id_producto: int, nueva_cantidad: int = None, nuevo_precio: float = None) -> bool:
        """Actualiza la cantidad y/o precio de un producto."""
        if id_producto not in self.__ids:
            print(f"\n⚠️  No se encontró un producto con ID {id_producto}.")
            return False
        producto = self.__productos[id_producto]
        cambios = []
        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)
            cambios.append(f"Cantidad → {nueva_cantidad}")
        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)
            cambios.append(f"Precio → ${nuevo_precio:,.2f}")
        if cambios:
            self.guardar_en_archivo()
            print(f"\n✏️  Producto '{producto.get_nombre()}' actualizado: {', '.join(cambios)}")
        return True

    def buscar_por_nombre(self, nombre: str) -> list[Producto]:
        """Busca productos cuyo nombre contenga la cadena dada (sin distinción de mayúsculas)."""
        nombre_lower = nombre.lower()
        resultados: list[Producto] = []
        for clave, ids in self.__indice_nombre.items():
            if nombre_lower in clave:
                for id_prod in ids:
                    resultados.append(self.__productos[id_prod])
        return resultados

    def obtener_producto(self, id_producto: int):
        """Retorna un producto por su ID o None si no existe."""
        return self.__productos.get(id_producto)

    def mostrar_todos(self):
        """Muestra todos los productos del inventario."""
        if not self.__productos:
            print("\n📦 El inventario está vacío.")
            return
        print("\n" + "=" * 65)
        print(f"{'INVENTARIO COMPLETO':^65}")
        print("=" * 65)
        # Tupla de encabezados para la tabla
        encabezados: tuple = ("ID", "Nombre", "Cantidad", "Precio")
        print(f"  {encabezados[0]:<6}{encabezados[1]:<25}{encabezados[2]:<12}{encabezados[3]:<15}")
        print("-" * 65)
        for producto in self.__productos.values():
            print(f"  {producto.get_id():<6}{producto.get_nombre():<25}"
                  f"{producto.get_cantidad():<12}${producto.get_precio():>10,.2f}")
        print("-" * 65)
        print(f"  Total de productos: {self.total_productos}")
        # Calcular valor total del inventario
        valor_total = sum(p.get_cantidad() * p.get_precio() for p in self.__productos.values())
        print(f"  Valor total del inventario: ${valor_total:,.2f}")
        print("=" * 65)

    # ── Índice de nombres (colección auxiliar) ──
    def __actualizar_indice_nombre(self, producto: Producto, agregar: bool):
        """Mantiene el índice invertido de nombres actualizado."""
        clave = producto.get_nombre().lower()
        if agregar:
            self.__indice_nombre.setdefault(clave, set()).add(producto.get_id())
        else:
            if clave in self.__indice_nombre:
                self.__indice_nombre[clave].discard(producto.get_id())
                if not self.__indice_nombre[clave]:
                    del self.__indice_nombre[clave]

    # ── Almacenamiento en archivos (serialización/deserialización) ──
    def guardar_en_archivo(self):
        """Serializa el inventario y lo guarda en un archivo JSON."""
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.ARCHIVO)
        datos = [producto.to_dict() for producto in self.__productos.values()]
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def cargar_desde_archivo(self):
        """Carga el inventario desde un archivo JSON si existe."""
        ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.ARCHIVO)
        if not os.path.exists(ruta):
            return
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            for item in datos:
                producto = Producto.from_dict(item)
                self.__productos[producto.get_id()] = producto
                self.__ids.add(producto.get_id())
                self.__actualizar_indice_nombre(producto, agregar=True)
            print(f"📂 Inventario cargado: {len(datos)} producto(s) recuperados.")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Error al cargar el inventario: {e}")

    def siguiente_id(self) -> int:
        """Genera el siguiente ID disponible."""
        return max(self.__ids, default=0) + 1


# ──────────────────────────────────────────────
# Interfaz de Usuario (Menú interactivo)
# ──────────────────────────────────────────────
def leer_entero(mensaje: str):
    """Lee un entero desde la consola con validación."""
    try:
        return int(input(mensaje))
    except ValueError:
        print("⚠️  Debe ingresar un número entero válido.")
        return None


def leer_flotante(mensaje: str):
    """Lee un flotante desde la consola con validación."""
    try:
        return float(input(mensaje))
    except ValueError:
        print("⚠️  Debe ingresar un número válido.")
        return None


def menu_agregar(inventario: Inventario):
    """Flujo para agregar un nuevo producto."""
    print("\n── Agregar Producto ──")
    id_sugerido = inventario.siguiente_id()
    print(f"   (ID sugerido: {id_sugerido})")
    id_prod = leer_entero("   ID del producto: ")
    if id_prod is None:
        return
    nombre = input("   Nombre: ").strip()
    if not nombre:
        print("⚠️  El nombre no puede estar vacío.")
        return
    cantidad = leer_entero("   Cantidad: ")
    if cantidad is None or cantidad < 0:
        print("⚠️  La cantidad debe ser un número entero positivo.")
        return
    precio = leer_flotante("   Precio: $")
    if precio is None or precio < 0:
        print("⚠️  El precio debe ser un número positivo.")
        return
    producto = Producto(id_prod, nombre, cantidad, precio)
    inventario.agregar_producto(producto)


def menu_eliminar(inventario: Inventario):
    """Flujo para eliminar un producto."""
    print("\n── Eliminar Producto ──")
    id_prod = leer_entero("   ID del producto a eliminar: ")
    if id_prod is None:
        return
    producto = inventario.obtener_producto(id_prod)
    if producto:
        print(f"   Producto encontrado: {producto}")
        confirmacion = input("   ¿Está seguro de eliminarlo? (s/n): ").strip().lower()
        if confirmacion == "s":
            inventario.eliminar_producto(id_prod)
        else:
            print("   Operación cancelada.")
    else:
        print(f"\n⚠️  No se encontró un producto con ID {id_prod}.")


def menu_actualizar(inventario: Inventario):
    """Flujo para actualizar un producto."""
    print("\n── Actualizar Producto ──")
    id_prod = leer_entero("   ID del producto a actualizar: ")
    if id_prod is None:
        return
    producto = inventario.obtener_producto(id_prod)
    if not producto:
        print(f"\n⚠️  No se encontró un producto con ID {id_prod}.")
        return
    print(f"   Producto actual: {producto}")
    print("   (Deje vacío para no modificar)")

    cant_input = input("   Nueva cantidad: ").strip()
    nueva_cantidad = None
    if cant_input:
        try:
            nueva_cantidad = int(cant_input)
            if nueva_cantidad < 0:
                print("⚠️  La cantidad no puede ser negativa.")
                return
        except ValueError:
            print("⚠️  Cantidad inválida.")
            return

    precio_input = input("   Nuevo precio: $").strip()
    nuevo_precio = None
    if precio_input:
        try:
            nuevo_precio = float(precio_input)
            if nuevo_precio < 0:
                print("⚠️  El precio no puede ser negativo.")
                return
        except ValueError:
            print("⚠️  Precio inválido.")
            return

    if nueva_cantidad is None and nuevo_precio is None:
        print("   No se realizaron cambios.")
        return

    inventario.actualizar_producto(id_prod, nueva_cantidad, nuevo_precio)


def menu_buscar(inventario: Inventario):
    """Flujo para buscar productos por nombre."""
    print("\n── Buscar Producto por Nombre ──")
    nombre = input("   Nombre a buscar: ").strip()
    if not nombre:
        print("⚠️  Debe ingresar un nombre para buscar.")
        return
    resultados = inventario.buscar_por_nombre(nombre)
    if not resultados:
        print(f"\n🔍 No se encontraron productos con el nombre '{nombre}'.")
    else:
        print(f"\n🔍 Se encontraron {len(resultados)} resultado(s):")
        print("-" * 65)
        for producto in resultados:
            print(f"   {producto}")
        print("-" * 65)


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n╔═══════════════════════════════════════════╗")
    print("║   SISTEMA DE GESTIÓN DE INVENTARIO        ║")
    print("╠═══════════════════════════════════════════╣")
    print("║   1. Agregar producto                     ║")
    print("║   2. Eliminar producto                    ║")
    print("║   3. Actualizar producto                  ║")
    print("║   4. Buscar producto por nombre            ║")
    print("║   5. Mostrar todos los productos          ║")
    print("║   6. Salir                                ║")
    print("╚═══════════════════════════════════════════╝")


def main():
    """Punto de entrada principal del programa."""
    inventario = Inventario()

    # Diccionario de acciones del menú (colección para mapear opciones)
    acciones: dict = {
        1: menu_agregar,
        2: menu_eliminar,
        3: menu_actualizar,
        4: menu_buscar,
        5: lambda inv: inv.mostrar_todos(),
    }

    while True:
        mostrar_menu()
        opcion = leer_entero("   Seleccione una opción: ")
        if opcion is None:
            continue
        if opcion == 6:
            print("\n👋 ¡Hasta luego! Inventario guardado correctamente.")
            break
        accion = acciones.get(opcion)
        if accion:
            accion(inventario)
        else:
            print("\n⚠️  Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()

