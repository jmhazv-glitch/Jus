"""
Módulo producto.py
Sistema Avanzado de Gestión de Inventario
Contiene la clase Producto que representa un artículo en el inventario.
"""
class Producto:
    """Representa un producto del inventario."""

    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # ── Getters ──
    def get_id(self) -> int:
        """Retorna el ID del producto."""
        return self.__id

    def get_nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self.__nombre

    def get_cantidad(self) -> int:
        """Retorna la cantidad disponible del producto."""
        return self.__cantidad

    def get_precio(self) -> float:
        """Retorna el precio del producto."""
        return self.__precio

    # ── Setters ──
    def set_nombre(self, nombre: str):
        """Establece un nuevo nombre para el producto."""
        self.__nombre = nombre

    def set_cantidad(self, cantidad: int):
        """Establece una nueva cantidad para el producto."""
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = cantidad

    def set_precio(self, precio: float):
        """Establece un nuevo precio para el producto."""
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.__precio = precio

    # ── Representación ──
    def __str__(self) -> str:
        """Representación en string del producto para visualización."""
        return (f"ID: {self.__id} | Nombre: {self.__nombre} | "
                f"Cantidad: {self.__cantidad} | Precio: ${self.__precio:,.2f}")

    def __repr__(self) -> str:
        """Representación oficial del producto."""
        return (f"Producto(id={self.__id}, nombre='{self.__nombre}', "
                f"cantidad={self.__cantidad}, precio={self.__precio})")

    # ── Serialización a diccionario (para colecciones) ──
    def to_dict(self) -> dict:
        """Serializa el producto a diccionario."""
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

    # ── Serialización a línea de texto (para archivo .txt) ──
    def to_line(self) -> str:
        """Convierte el producto a una línea de texto con formato id|nombre|cantidad|precio."""
        return f"{self.__id}|{self.__nombre}|{self.__cantidad}|{self.__precio}"

    @staticmethod
    def from_line(linea: str) -> "Producto":
        """Crea un Producto a partir de una línea de texto con formato id|nombre|cantidad|precio."""
        try:
            partes = linea.strip().split('|')
            if len(partes) != 4:
                raise ValueError(f"Formato inválido: se esperaban 4 campos, se encontraron {len(partes)}")
            id_producto = int(partes[0])
            nombre = partes[1]
            cantidad = int(partes[2])
            precio = float(partes[3])
            return Producto(id_producto, nombre, cantidad, precio)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Error al parsear línea '{linea}': {e}")

