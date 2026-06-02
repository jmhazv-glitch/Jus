"""
Módulo Usuario - Representa un usuario de la biblioteca digital.

Utiliza una lista para gestionar los libros prestados a cada usuario,
permitiendo agregar y eliminar libros dinámicamente.
"""

from libro import Libro


class Usuario:


    def __init__(self, nombre: str, id_usuario: str):

        self._nombre: str = nombre
        self._id_usuario: str = id_usuario
        # Lista mutable para gestionar los libros prestados dinámicamente
        self._libros_prestados: list[Libro] = []

    # --- Propiedades ---

    @property
    def nombre(self) -> str:
        """Retorna el nombre del usuario."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Permite actualizar el nombre del usuario."""
        self._nombre = valor

    @property
    def id_usuario(self) -> str:
        """Retorna el ID único del usuario."""
        return self._id_usuario

    @property
    def libros_prestados(self) -> list:
        """Retorna la lista de libros actualmente prestados."""
        return self._libros_prestados.copy()  # Copia para evitar modificaciones externas

    @property
    def cantidad_libros_prestados(self) -> int:
        """Retorna la cantidad de libros actualmente prestados."""
        return len(self._libros_prestados)

    # --- Métodos de gestión de préstamos ---

    def agregar_libro_prestado(self, libro: Libro) -> bool:

        # Verificar que el usuario no tenga ya este libro
        if any(l.isbn == libro.isbn for l in self._libros_prestados):
            print(f"  ⚠️  El usuario '{self._nombre}' ya tiene prestado el libro '{libro.titulo}'.")
            return False

        self._libros_prestados.append(libro)
        return True

    def eliminar_libro_prestado(self, isbn: str) -> Libro | None:

        for i, libro in enumerate(self._libros_prestados):
            if libro.isbn == isbn:
                return self._libros_prestados.pop(i)

        print(f"   El usuario '{self._nombre}' no tiene prestado un libro con ISBN '{isbn}'.")
        return None

    def tiene_libro(self, isbn: str) -> bool:
        """Verifica si el usuario tiene un libro prestado por su ISBN."""
        return any(l.isbn == isbn for l in self._libros_prestados)

    # --- Métodos especiales ---

    def __str__(self) -> str:
        """Representación en cadena legible del usuario."""
        prestados = self.cantidad_libros_prestados
        return (f"{self._nombre} (ID: {self._id_usuario}) | "
                f"Libros prestados: {prestados}")

    def __repr__(self) -> str:
        """Representación técnica del usuario."""
        return f"Usuario(nombre='{self._nombre}', id_usuario='{self._id_usuario}')"

    def __eq__(self, otro) -> bool:
        """Dos usuarios son iguales si tienen el mismo ID."""
        if isinstance(otro, Usuario):
            return self._id_usuario == otro._id_usuario
        return False

    def __hash__(self) -> int:
        """Hash basado en el ID de usuario."""
        return hash(self._id_usuario)

