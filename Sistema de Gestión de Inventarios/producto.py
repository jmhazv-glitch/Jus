"""
Módulo producto.py
Contiene la clase Producto que representa un artículo en el inventario.
"""

class Producto:
    
    def __init__(self, id, nombre, cantidad, precio):
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

    def to_line(self):

        return f"{self.__id}|{self.__nombre}|{self.__cantidad}|{self.__precio}"

    @staticmethod
    def from_line(linea):
        try:
            partes = linea.strip().split('|')
            if len(partes) != 4:
                raise ValueError(f"Formato inválido: se esperaban 4 campos, se encontraron {len(partes)}")

            id = int(partes[0])
            nombre = partes[1]
            cantidad = int(partes[2])
            precio = float(partes[3])

            return Producto(id, nombre, cantidad, precio)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error al parsear línea de producto: {e}")
