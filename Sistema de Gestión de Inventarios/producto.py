"""
Módulo producto.py
Contiene la clase Producto que representa un artículo en el inventario.
"""

class Producto:
    """
    Clase que representa un producto en el inventario.
    
    Atributos:
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        cantidad (int): Cantidad disponible en stock
        precio (float): Precio unitario del producto
    """
    
    def __init__(self, id, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.
        
        Args:
            id (int): ID único del producto
            nombre (str): Nombre descriptivo del producto
            cantidad (int): Cantidad inicial en inventario
            precio (float): Precio por unidad
        """
        self.__id = id
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio
    
    # Getters
    def get_id(self):
        """Retorna el ID del producto."""
        return self.__id
    
    def get_nombre(self):
        """Retorna el nombre del producto."""
        return self.__nombre
    
    def get_cantidad(self):
        """Retorna la cantidad disponible del producto."""
        return self.__cantidad
    
    def get_precio(self):
        """Retorna el precio del producto."""
        return self.__precio
    
    # Setters
    def set_id(self, id):
        """
        Establece un nuevo ID para el producto.
        
        Args:
            id (int): Nuevo ID del producto
        """
        self.__id = id
    
    def set_nombre(self, nombre):
        """
        Establece un nuevo nombre para el producto.
        
        Args:
            nombre (str): Nuevo nombre del producto
        """
        self.__nombre = nombre
    
    def set_cantidad(self, cantidad):
        """
        Establece una nueva cantidad para el producto.
        
        Args:
            cantidad (int): Nueva cantidad en inventario
        """
        self.__cantidad = cantidad
    
    def set_precio(self, precio):
        """
        Establece un nuevo precio para el producto.
        
        Args:
            precio (float): Nuevo precio del producto
        """
        self.__precio = precio
    
    def __str__(self):
        """
        Representación en string del producto para visualización.
        
        Returns:
            str: Información formateada del producto
        """
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"
    
    def __repr__(self):
        """
        Representación oficial del producto.
        
        Returns:
            str: Representación del objeto Producto
        """
        return f"Producto(id={self.__id}, nombre='{self.__nombre}', cantidad={self.__cantidad}, precio={self.__precio})"
