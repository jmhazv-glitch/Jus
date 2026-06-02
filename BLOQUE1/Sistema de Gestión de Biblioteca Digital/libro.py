"""
Módulo Libro - Representa un libro en la biblioteca digital.

Utiliza una tupla para almacenar el par (autor, título) ya que estos
atributos son inmutables una vez creado el libro.
"""
class Libro:

    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str):

        # Tupla inmutable para almacenar autor y título (no cambian una vez creados)
        self._info_libro: tuple = (autor, titulo)
        self._categoria: str = categoria
        self._isbn: str = isbn
        self._disponible: bool = True  # Por defecto, el libro está disponible

    # --- Propiedades de solo lectura ---

    @property
    def titulo(self) -> str:
        """Retorna el título del libro desde la tupla inmutable."""
        return self._info_libro[1]

    @property
    def autor(self) -> str:
        """Retorna el autor del libro desde la tupla inmutable."""
        return self._info_libro[0]

    @property
    def info_libro(self) -> tuple:
        """Retorna la tupla inmutable (autor, título)."""
        return self._info_libro

    @property
    def categoria(self) -> str:
        """Retorna la categoría del libro."""
        return self._categoria

    @property
    def isbn(self) -> str:
        """Retorna el ISBN del libro."""
        return self._isbn

    @property
    def disponible(self) -> bool:
        """Retorna si el libro está disponible para préstamo."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        """Establece la disponibilidad del libro."""
        self._disponible = valor

    # --- Métodos especiales ---

    def __str__(self) -> str:
        """Representación en cadena legible del libro."""
        estado = "Disponible" if self._disponible else "Prestado"
        return (f"📖 '{self.titulo}' por {self.autor} | "
                f"Categoría: {self.categoria} | ISBN: {self.isbn} | {estado}")

    def __repr__(self) -> str:
        """Representación técnica del libro."""
        return (f"Libro(titulo='{self.titulo}', autor='{self.autor}', "
                f"categoria='{self.categoria}', isbn='{self.isbn}')")

    def __eq__(self, otro) -> bool:
        """Dos libros son iguales si tienen el mismo ISBN."""
        if isinstance(otro, Libro):
            return self._isbn == otro._isbn
        return False

    def __hash__(self) -> int:
        """Hash basado en el ISBN para uso en conjuntos y diccionarios."""
        return hash(self._isbn)

