"""
Módulo inventario.py
Contiene la clase Inventario que gestiona la colección de productos.
Incluye persistencia en archivos y manejo de excepciones.
"""

from producto import Producto
import os

class ArchivoInventarioError(Exception):
    """Excepción personalizada para errores relacionados con el archivo de inventario."""
    pass

class Inventario:
    """
    Clase que gestiona el inventario de productos con persistencia en archivo.

    Atributos:
        productos (list): Lista de objetos Producto
        archivo (str): Ruta del archivo de inventario
    """
    
    # Ruta por defecto del archivo de inventario
    ARCHIVO_DEFAULT = "inventario.txt"

    def __init__(self, archivo=None):
        """
        Constructor que inicializa el inventario.
        Intenta cargar productos desde el archivo si existe.

        Args:
            archivo (str, optional): Ruta del archivo de inventario.
                                     Por defecto usa 'inventario.txt'
        """
        self.__productos = []
        self.__archivo = archivo if archivo else self.ARCHIVO_DEFAULT
        self.__ultimo_error = None  # Almacena el último error ocurrido

        # Intentar cargar el inventario desde el archivo al iniciar
        self._cargar_desde_archivo()

    def get_ultimo_error(self):
        """
        Retorna el último error ocurrido en operaciones de archivo.

        Returns:
            str: Mensaje del último error o None si no hay error
        """
        return self.__ultimo_error

    def _cargar_desde_archivo(self):
        """
        Carga los productos desde el archivo de inventario.

        Este método maneja las siguientes excepciones:
        - FileNotFoundError: El archivo no existe (se creará al guardar)
        - PermissionError: No hay permisos de lectura
        - ValueError: Datos corruptos en el archivo

        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado de la operación
        """
        self.__ultimo_error = None
        productos_cargados = 0
        lineas_con_error = 0

        try:
            # Verificar si el archivo existe
            if not os.path.exists(self.__archivo):
                mensaje = f"📁 Archivo '{self.__archivo}' no encontrado. Se creará uno nuevo al agregar productos."
                return (True, mensaje)

            # Abrir y leer el archivo
            with open(self.__archivo, 'r', encoding='utf-8') as archivo:
                for num_linea, linea in enumerate(archivo, 1):
                    # Ignorar líneas vacías o comentarios
                    linea = linea.strip()
                    if not linea or linea.startswith('#'):
                        continue

                    try:
                        producto = Producto.from_line(linea)
                        # Verificar que el ID sea único
                        if not any(p.get_id() == producto.get_id() for p in self.__productos):
                            self.__productos.append(producto)
                            productos_cargados += 1
                        else:
                            lineas_con_error += 1
                            print(f"⚠️  Línea {num_linea}: ID duplicado ignorado")
                    except ValueError as e:
                        lineas_con_error += 1
                        print(f"⚠️  Línea {num_linea}: {e}")

            if lineas_con_error > 0:
                mensaje = f"✅ Se cargaron {productos_cargados} productos. ⚠️  {lineas_con_error} líneas con errores ignoradas."
            else:
                mensaje = f"✅ Se cargaron {productos_cargados} productos desde '{self.__archivo}'."

            return (True, mensaje)

        except PermissionError:
            self.__ultimo_error = f"❌ Error: No tiene permisos para leer el archivo '{self.__archivo}'."
            return (False, self.__ultimo_error)

        except IOError as e:
            self.__ultimo_error = f"❌ Error de entrada/salida al leer '{self.__archivo}': {e}"
            return (False, self.__ultimo_error)

        except Exception as e:
            self.__ultimo_error = f"❌ Error inesperado al cargar inventario: {e}"
            return (False, self.__ultimo_error)

    def _guardar_en_archivo(self):
        """
        Guarda todos los productos en el archivo de inventario.

        Este método maneja las siguientes excepciones:
        - PermissionError: No hay permisos de escritura
        - IOError: Error de entrada/salida

        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado de la operación
        """
        self.__ultimo_error = None

        try:
            with open(self.__archivo, 'w', encoding='utf-8') as archivo:
                # Escribir encabezado informativo
                archivo.write("# Archivo de Inventario - Sistema de Gestión de Inventarios\n")
                archivo.write("# Formato: id|nombre|cantidad|precio\n")
                archivo.write("# No editar manualmente este archivo\n")
                archivo.write("#" + "="*50 + "\n")

                # Escribir cada producto
                for producto in self.__productos:
                    archivo.write(producto.to_line() + "\n")

            mensaje = f"💾 Inventario guardado exitosamente en '{self.__archivo}'."
            return (True, mensaje)

        except PermissionError:
            self.__ultimo_error = f"❌ Error: No tiene permisos para escribir en '{self.__archivo}'."
            return (False, self.__ultimo_error)

        except IOError as e:
            self.__ultimo_error = f"❌ Error de entrada/salida al guardar '{self.__archivo}': {e}"
            return (False, self.__ultimo_error)

        except Exception as e:
            self.__ultimo_error = f"❌ Error inesperado al guardar inventario: {e}"
            return (False, self.__ultimo_error)

    def cargar_inventario(self):
        """
        Método público para cargar/recargar el inventario desde archivo.

        Returns:
            tuple: (bool exito, str mensaje)
        """
        self.__productos = []  # Limpiar lista actual
        return self._cargar_desde_archivo()

    def agregar_producto(self, producto):
        """
        Añade un nuevo producto al inventario y guarda en archivo.
        Verifica que el ID sea único antes de agregar.

        Args:
            producto (Producto): Objeto Producto a añadir

        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado
        """
        # Verificar que el ID sea único
        for p in self.__productos:
            if p.get_id() == producto.get_id():
                return (False, f"❌ Error: Ya existe un producto con el ID {producto.get_id()}.")

        self.__productos.append(producto)

        # Guardar cambios en archivo
        exito, mensaje_archivo = self._guardar_en_archivo()

        if exito:
            return (True, f"✅ Producto '{producto.get_nombre()}' agregado exitosamente!\n{mensaje_archivo}")
        else:
            # Si falla el guardado, revertir el cambio en memoria
            self.__productos.pop()
            return (False, f"❌ No se pudo agregar el producto. {mensaje_archivo}")

    def eliminar_producto(self, id):
        """
        Elimina un producto del inventario por su ID y actualiza el archivo.

        Args:
            id (int): ID del producto a eliminar
            
        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado
        """
        for i, producto in enumerate(self.__productos):
            if producto.get_id() == id:
                producto_eliminado = self.__productos.pop(i)

                # Guardar cambios en archivo
                exito, mensaje_archivo = self._guardar_en_archivo()

                if exito:
                    return (True, f"✅ Producto '{producto_eliminado.get_nombre()}' eliminado exitosamente!\n{mensaje_archivo}")
                else:
                    # Si falla el guardado, revertir el cambio
                    self.__productos.insert(i, producto_eliminado)
                    return (False, f"❌ No se pudo eliminar el producto. {mensaje_archivo}")

        return (False, f"❌ Error: No se encontró un producto con el ID {id}.")

    def actualizar_cantidad(self, id, nueva_cantidad):
        """
        Actualiza la cantidad de un producto específico y guarda en archivo.

        Args:
            id (int): ID del producto a actualizar
            nueva_cantidad (int): Nueva cantidad para el producto
            
        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado
        """
        for producto in self.__productos:
            if producto.get_id() == id:
                cantidad_anterior = producto.get_cantidad()
                producto.set_cantidad(nueva_cantidad)

                # Guardar cambios en archivo
                exito, mensaje_archivo = self._guardar_en_archivo()

                if exito:
                    return (True, f"✅ Cantidad actualizada exitosamente!\n{mensaje_archivo}")
                else:
                    # Si falla, revertir el cambio
                    producto.set_cantidad(cantidad_anterior)
                    return (False, f"❌ No se pudo actualizar la cantidad. {mensaje_archivo}")

        return (False, f"❌ Error: No se encontró un producto con el ID {id}.")

    def actualizar_precio(self, id, nuevo_precio):
        """
        Actualiza el precio de un producto específico y guarda en archivo.

        Args:
            id (int): ID del producto a actualizar
            nuevo_precio (float): Nuevo precio para el producto
            
        Returns:
            tuple: (bool exito, str mensaje) indicando el resultado
        """
        for producto in self.__productos:
            if producto.get_id() == id:
                precio_anterior = producto.get_precio()
                producto.set_precio(nuevo_precio)

                # Guardar cambios en archivo
                exito, mensaje_archivo = self._guardar_en_archivo()

                if exito:
                    return (True, f"✅ Precio actualizado exitosamente!\n{mensaje_archivo}")
                else:
                    # Si falla, revertir el cambio
                    producto.set_precio(precio_anterior)
                    return (False, f"❌ No se pudo actualizar el precio. {mensaje_archivo}")

        return (False, f"❌ Error: No se encontró un producto con el ID {id}.")

    def buscar_por_nombre(self, nombre):
        """
        Busca productos por nombre (búsqueda parcial, no case-sensitive).

        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            list: Lista de productos que coinciden con la búsqueda
        """
        resultados = []
        nombre_lower = nombre.lower()
        
        for producto in self.__productos:
            if nombre_lower in producto.get_nombre().lower():
                resultados.append(producto)
        
        return resultados
    
    def buscar_por_id(self, id):
        """
        Busca un producto específico por su ID.

        Args:
            id (int): ID del producto a buscar
            
        Returns:
            Producto: El producto encontrado o None si no existe
        """
        for producto in self.__productos:
            if producto.get_id() == id:
                return producto
        return None
    
    def mostrar_todos(self):
        """
        Retorna todos los productos en el inventario.
        
        Returns:
            list: Lista con todos los productos
        """
        return self.__productos.copy()
    
    def obtener_total_productos(self):
        """
        Retorna el número total de productos en el inventario.

        Returns:
            int: Cantidad de productos diferentes en inventario
        """
        return len(self.__productos)
    
    def obtener_valor_total_inventario(self):
        """
        Calcula el valor total del inventario (suma de precio * cantidad de todos los productos).
        
        Returns:
            float: Valor total del inventario
        """
        valor_total = 0
        for producto in self.__productos:
            valor_total += producto.get_precio() * producto.get_cantidad()
        return valor_total
    
    def get_ruta_archivo(self):
        """
        Retorna la ruta del archivo de inventario.

        Returns:
            str: Ruta del archivo de inventario
        """
        return self.__archivo

    def __str__(self):
        """
        Representación en string del inventario.

        Returns:
            str: Resumen del inventario
        """
        return f"Inventario con {len(self.__productos)} productos (archivo: {self.__archivo})"
