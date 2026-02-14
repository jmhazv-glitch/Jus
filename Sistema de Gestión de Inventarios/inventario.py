"""
Modulo inventario.py
Contiene la clase Inventario que gestiona la colección de productos.
"""

from producto import Producto

class Inventario:
    """
    Clase que gestiona el inventario de productos.
    
    Atributos:
        productos (list): Lista de objetos Producto
    """
    
    def __init__(self):
        """Constructor que inicializa una lista vacía de productos."""
        self.__productos = []
    
    def agregar_producto(self, producto):
        """
        Añade un nuevo producto al inventario.
        Verifica que el ID sea único antes de agregar.
        
        Args:
            producto (Producto): Objeto Producto a añadir
            
        Returns:
            bool: True si se agregó exitosamente, False si el ID ya existe
        """
        # Verificar que el ID sea único
        for p in self.__productos:
            if p.get_id() == producto.get_id():
                return False
        
        self.__productos.append(producto)
        return True
    
    def eliminar_producto(self, id):
        """
        Elimina un producto del inventario por su ID.
        
        Args:
            id (int): ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False si no se encontró
        """
        for i, producto in enumerate(self.__productos):
            if producto.get_id() == id:
                self.__productos.pop(i)
                return True
        return False
    
    def actualizar_cantidad(self, id, nueva_cantidad):
        """
        Actualiza la cantidad de un producto específico.
        
        Args:
            id (int): ID del producto a actualizar
            nueva_cantidad (int): Nueva cantidad para el producto
            
        Returns:
            bool: True si se actualizó exitosamente, False si no se encontró
        """
        for producto in self.__productos:
            if producto.get_id() == id:
                producto.set_cantidad(nueva_cantidad)
                return True
        return False
    
    def actualizar_precio(self, id, nuevo_precio):
        """
        Actualiza el precio de un producto específico.
        
        Args:
            id (int): ID del producto a actualizar
            nuevo_precio (float): Nuevo precio para el producto
            
        Returns:
            bool: True si se actualizó exitosamente, False si no se encontró
        """
        for producto in self.__productos:
            if producto.get_id() == id:
                producto.set_precio(nuevo_precio)
                return True
        return False
    
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
    
    def __str__(self):
        """
        Representación en string del inventario.
        
        Returns:
            str: Resumen del inventario
        """
        return f"Inventario con {len(self.__productos)} productos"
