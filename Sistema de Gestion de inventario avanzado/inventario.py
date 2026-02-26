"""
Módulo inventario.py
"""
from producto import Producto
import os
class ArchivoInventarioError(Exception):
    """Excepción personalizada para errores relacionados con el archivo de inventario."""
    pass
class Inventario:
    """
    Gestiona la colección de productos del inventario con persistencia en archivo.

    Colecciones utilizadas:
        - dict {id: Producto}  → búsqueda rápida O(1) por ID
        - set {ids}            → validación de unicidad rápida
        - dict {nombre: set}   → índice invertido para búsqueda por nombre
    """

    ARCHIVO_DEFAULT = "inventario.txt"

    def __init__(self, archivo=None):
        """
        Constructor que inicializa el inventario.
        Intenta cargar productos desde el archivo si existe.

        Args:
            archivo (str, optional): Ruta del archivo de inventario.
                                     Por defecto usa 'inventario.txt'
        """
        # Diccionario {id: Producto} → búsqueda rápida O(1)
        self.__productos: dict[int, Producto] = {}
        # Conjunto de IDs para validar unicidad rápidamente
        self.__ids: set[int] = set()
        # Índice invertido nombre→set(ids) para búsqueda por nombre
        self.__indice_nombre: dict[str, set[int]] = {}
        # Ruta del archivo
        self.__archivo = archivo if archivo else self.ARCHIVO_DEFAULT
        # Último error ocurrido
        self.__ultimo_error = None
        # Cargar datos persistentes al iniciar
        self._cargar_desde_archivo()

    # ── Propiedades de consulta ──
    @property
    def total_productos(self) -> int:
        """Retorna el número total de productos en el inventario."""
        return len(self.__productos)

    def get_ultimo_error(self):
        """Retorna el último error ocurrido en operaciones de archivo."""
        return self.__ultimo_error

    # ── Métodos principales ──
    def agregar_producto(self, producto: Producto) -> tuple:
        """
        Añade un nuevo producto al inventario y guarda en archivo.

        Args:
            producto (Producto): Objeto Producto a añadir

        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado
        """
        if producto.get_id() in self.__ids:
            return (False, f" Error: Ya existe un producto con el ID {producto.get_id()}.")

        self.__productos[producto.get_id()] = producto
        self.__ids.add(producto.get_id())
        self.__actualizar_indice_nombre(producto, agregar=True)

        # Guardar cambios en archivo
        exito, mensaje_archivo = self._guardar_en_archivo()
        if exito:
            return (True, f" Producto '{producto.get_nombre()}' agregado exitosamente!\n{mensaje_archivo}")
        else:
            # Revertir si falla el guardado
            del self.__productos[producto.get_id()]
            self.__ids.discard(producto.get_id())
            self.__actualizar_indice_nombre(producto, agregar=False)
            return (False, f" No se pudo agregar el producto. {mensaje_archivo}")

    def eliminar_producto(self, id_producto: int) -> tuple:
        """
        Elimina un producto por su ID y actualiza el archivo.

        Args:
            id_producto (int): ID del producto a eliminar

        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado
        """
        if id_producto not in self.__ids:
            return (False, f" Error: No se encontró un producto con el ID {id_producto}.")

        producto = self.__productos[id_producto]
        nombre = producto.get_nombre()

        # Eliminar de las colecciones
        self.__actualizar_indice_nombre(producto, agregar=False)
        del self.__productos[id_producto]
        self.__ids.discard(id_producto)

        # Guardar cambios en archivo
        exito, mensaje_archivo = self._guardar_en_archivo()
        if exito:
            return (True, f" Producto '{nombre}' eliminado correctamente.\n{mensaje_archivo}")
        else:
            # Revertir si falla el guardado
            self.__productos[id_producto] = producto
            self.__ids.add(id_producto)
            self.__actualizar_indice_nombre(producto, agregar=True)
            return (False, f" No se pudo eliminar el producto. {mensaje_archivo}")

    def actualizar_cantidad(self, id_producto: int, nueva_cantidad: int) -> tuple:
        """
        Actualiza la cantidad de un producto.

        Args:
            id_producto (int): ID del producto
            nueva_cantidad (int): Nueva cantidad

        Returns:
            tuple: (bool exito, str mensaje)
        """
        if id_producto not in self.__ids:
            return (False, f" Error: No se encontró un producto con el ID {id_producto}.")

        producto = self.__productos[id_producto]
        cantidad_anterior = producto.get_cantidad()
        producto.set_cantidad(nueva_cantidad)

        exito, mensaje_archivo = self._guardar_en_archivo()
        if exito:
            return (True, f"  Cantidad de '{producto.get_nombre()}' actualizada: "
                          f"{cantidad_anterior} → {nueva_cantidad}\n{mensaje_archivo}")
        else:
            producto.set_cantidad(cantidad_anterior)
            return (False, f" No se pudo actualizar. {mensaje_archivo}")

    def actualizar_precio(self, id_producto: int, nuevo_precio: float) -> tuple:
        """
        Actualiza el precio de un producto.

        Args:
            id_producto (int): ID del producto
            nuevo_precio (float): Nuevo precio

        Returns:
            tuple: (bool exito, str mensaje)
        """
        if id_producto not in self.__ids:
            return (False, f" Error: No se encontró un producto con el ID {id_producto}.")

        producto = self.__productos[id_producto]
        precio_anterior = producto.get_precio()
        producto.set_precio(nuevo_precio)

        exito, mensaje_archivo = self._guardar_en_archivo()
        if exito:
            return (True, f"  Precio de '{producto.get_nombre()}' actualizado: "
                          f"${precio_anterior:,.2f} → ${nuevo_precio:,.2f}\n{mensaje_archivo}")
        else:
            producto.set_precio(precio_anterior)
            return (False, f" No se pudo actualizar. {mensaje_archivo}")

    def buscar_por_nombre(self, nombre: str) -> list[Producto]:
        """
        Busca productos cuyo nombre contenga la cadena dada (sin distinción de mayúsculas).
        Utiliza el índice invertido para optimizar la búsqueda.

        Args:
            nombre (str): Nombre o parte del nombre a buscar

        Returns:
            list: Lista de productos encontrados
        """
        nombre_lower = nombre.lower()
        resultados: list[Producto] = []
        for clave, ids in self.__indice_nombre.items():
            if nombre_lower in clave:
                for id_prod in ids:
                    resultados.append(self.__productos[id_prod])
        return resultados

    def buscar_por_id(self, id_producto: int):
        """
        Retorna un producto por su ID o None si no existe.
        Búsqueda O(1) gracias al diccionario.

        Args:
            id_producto (int): ID del producto a buscar

        Returns:
            Producto o None
        """
        return self.__productos.get(id_producto)

    def mostrar_todos(self):
        """Muestra todos los productos del inventario en formato tabla."""
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
        valor_total = sum(p.get_cantidad() * p.get_precio() for p in self.__productos.values())
        print(f"  Valor total del inventario: ${valor_total:,.2f}")
        print("=" * 65)

    def mostrar_estadisticas(self):
        """Muestra estadísticas generales del inventario."""
        if not self.__productos:
            print("\n📦 El inventario está vacío. No hay estadísticas disponibles.")
            return

        productos = list(self.__productos.values())
        total = self.total_productos
        cantidad_total = sum(p.get_cantidad() for p in productos)
        valor_total = sum(p.get_cantidad() * p.get_precio() for p in productos)
        precio_max = max(productos, key=lambda p: p.get_precio())
        precio_min = min(productos, key=lambda p: p.get_precio())
        mas_stock = max(productos, key=lambda p: p.get_cantidad())
        menos_stock = min(productos, key=lambda p: p.get_cantidad())

        print("\n" + "=" * 65)
        print(f"{'ESTADÍSTICAS DEL INVENTARIO':^65}")
        print("=" * 65)
        print(f"  Total de productos diferentes:  {total}")
        print(f"  Cantidad total de unidades:     {cantidad_total}")
        print(f"  Valor total del inventario:     ${valor_total:,.2f}")
        print("-" * 65)
        print(f"  Producto más caro:    {precio_max.get_nombre()} (${precio_max.get_precio():,.2f})")
        print(f"  Producto más barato:  {precio_min.get_nombre()} (${precio_min.get_precio():,.2f})")
        print(f"  Mayor stock:          {mas_stock.get_nombre()} ({mas_stock.get_cantidad()} uds.)")
        print(f"  Menor stock:          {menos_stock.get_nombre()} ({menos_stock.get_cantidad()} uds.)")
        print("=" * 65)

    def siguiente_id(self) -> int:
        """Genera el siguiente ID disponible."""
        return max(self.__ids, default=0) + 1

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
    def _guardar_en_archivo(self) -> tuple:
        """
        Guarda todos los productos en el archivo inventario.txt.
        Formato: id|nombre|cantidad|precio

        Returns:
            tuple: (bool exito, str mensaje)
        """
        self.__ultimo_error = None
        try:
            ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.__archivo)
            with open(ruta, 'w', encoding='utf-8') as archivo:
                # Escribir encabezado informativo
                archivo.write("# Archivo de Inventario - Sistema Avanzado de Gestión de Inventarios\n")
                archivo.write("# Formato: id|nombre|cantidad|precio\n")
                archivo.write("# No editar manualmente este archivo\n")
                archivo.write("#" + "=" * 50 + "\n")

                # Escribir cada producto
                for producto in self.__productos.values():
                    archivo.write(producto.to_line() + "\n")

            return (True, f" Inventario guardado exitosamente en '{self.__archivo}'.")

        except PermissionError:
            self.__ultimo_error = f" Error: No tiene permisos para escribir en '{self.__archivo}'."
            return (False, self.__ultimo_error)
        except IOError as e:
            self.__ultimo_error = f" Error de entrada/salida al guardar '{self.__archivo}': {e}"
            return (False, self.__ultimo_error)
        except Exception as e:
            self.__ultimo_error = f" Error inesperado al guardar inventario: {e}"
            return (False, self.__ultimo_error)

    def _cargar_desde_archivo(self) -> tuple:
        """
        Carga los productos desde el archivo inventario.txt.
        Formato esperado: id|nombre|cantidad|precio

        Returns:
            tuple: (bool exito, str mensaje)
        """
        self.__ultimo_error = None
        productos_cargados = 0
        lineas_con_error = 0

        try:
            ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.__archivo)

            if not os.path.exists(ruta):
                mensaje = f" Archivo '{self.__archivo}' no encontrado. Se creará uno nuevo al agregar productos."
                print(mensaje)
                return (True, mensaje)

            with open(ruta, 'r', encoding='utf-8') as archivo:
                for num_linea, linea in enumerate(archivo, 1):
                    linea = linea.strip()
                    # Ignorar líneas vacías o comentarios
                    if not linea or linea.startswith('#'):
                        continue

                    try:
                        producto = Producto.from_line(linea)
                        # Verificar que el ID sea único
                        if producto.get_id() not in self.__ids:
                            self.__productos[producto.get_id()] = producto
                            self.__ids.add(producto.get_id())
                            self.__actualizar_indice_nombre(producto, agregar=True)
                            productos_cargados += 1
                        else:
                            lineas_con_error += 1
                            print(f"  Línea {num_linea}: ID duplicado ignorado")
                    except ValueError as e:
                        lineas_con_error += 1
                        print(f"  Línea {num_linea}: {e}")

            if lineas_con_error > 0:
                mensaje = (f" Se cargaron {productos_cargados} productos. "
                           f"  {lineas_con_error} líneas con errores ignoradas.")
            else:
                mensaje = f" Se cargaron {productos_cargados} productos desde '{self.__archivo}'."

            print(mensaje)
            return (True, mensaje)

        except PermissionError:
            self.__ultimo_error = f" Error: No tiene permisos para leer el archivo '{self.__archivo}'."
            print(self.__ultimo_error)
            return (False, self.__ultimo_error)
        except IOError as e:
            self.__ultimo_error = f" Error de entrada/salida al leer '{self.__archivo}': {e}"
            print(self.__ultimo_error)
            return (False, self.__ultimo_error)
        except Exception as e:
            self.__ultimo_error = f" Error inesperado al cargar inventario: {e}"
            print(self.__ultimo_error)
            return (False, self.__ultimo_error)

    def cargar_inventario(self) -> tuple:
        """Método público para cargar/recargar el inventario desde archivo."""
        self.__productos = {}
        self.__ids = set()
        self.__indice_nombre = {}
        return self._cargar_desde_archivo()

