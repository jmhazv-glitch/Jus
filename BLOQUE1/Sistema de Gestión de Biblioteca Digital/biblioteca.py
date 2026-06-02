"""
Módulo Biblioteca - Gestiona la colección de libros, usuarios y préstamos.

Estructuras de datos utilizadas:
    - Diccionario (dict): Para almacenar libros por ISBN → acceso O(1).
    - Conjunto (set): Para garantizar IDs de usuario únicos.
    - Diccionario (dict): Para almacenar usuarios por ID → acceso O(1).
"""

from libro import Libro
from usuario import Usuario

class Biblioteca:

    def __init__(self, nombre: str):
        """
        Constructor de la biblioteca.

        Args:
            nombre (str): Nombre de la biblioteca.
        """
        self._nombre: str = nombre
        # Diccionario para búsqueda eficiente de libros por ISBN (O(1))
        self._catalogo: dict[str, Libro] = {}
        # Conjunto para asegurar que los IDs de usuario sean únicos
        self._ids_usuarios: set[str] = set()
        # Diccionario para acceso eficiente a usuarios por ID
        self._usuarios: dict[str, Usuario] = {}
        # Historial de préstamos y devoluciones
        self._historial_prestamos: list[dict] = []

    # --- Propiedades ---

    @property
    def nombre(self) -> str:
        """Retorna el nombre de la biblioteca."""
        return self._nombre

    @property
    def total_libros(self) -> int:
        """Retorna el total de libros en el catálogo."""
        return len(self._catalogo)

    @property
    def total_usuarios(self) -> int:
        """Retorna el total de usuarios registrados."""
        return len(self._usuarios)

    @property
    def libros_disponibles(self) -> int:
        """Retorna la cantidad de libros disponibles para préstamo."""
        return sum(1 for libro in self._catalogo.values() if libro.disponible)

    # =========================================================================
    # GESTIÓN DE LIBROS
    # =========================================================================

    def agregar_libro(self, libro: Libro) -> bool:

        if libro.isbn in self._catalogo:
            print(f" "
                  f" Ya existe un libro con ISBN '{libro.isbn}' en el catálogo.")
            return False

        # Inserción O(1) en el diccionario usando ISBN como clave
        self._catalogo[libro.isbn] = libro
        print(f" "
              f" Libro '{libro.titulo}' agregado al catálogo exitosamente.")
        return True

    def eliminar_libro(self, isbn: str) -> Libro | None:
        """
        Elimina un libro del catálogo por su ISBN.

        Verifica que el libro no esté prestado antes de eliminarlo.

        Args:
            isbn (str): El ISBN del libro a eliminar.

        Returns:
            Libro | None: El libro eliminado, o None si no se pudo eliminar.
        """
        if isbn not in self._catalogo:
            print(f" "
                  f" No se encontró un libro con ISBN '{isbn}' en el catálogo.")
            return None

        libro = self._catalogo[isbn]
        if not libro.disponible:
            print(f" "
                  f" No se puede eliminar '{libro.titulo}' porque está prestado.")
            return None

        # Eliminación O(1) del diccionario
        del self._catalogo[isbn]
        print(f" "
              f" Libro '{libro.titulo}' eliminado del catálogo exitosamente.")
        return libro

    # =========================================================================
    # GESTIÓN DE USUARIOS
    # =========================================================================

    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un nuevo usuario en la biblioteca.

        Usa un conjunto (set) para verificar unicidad de IDs de forma eficiente.

        Args:
            usuario (Usuario): El usuario a registrar.

        Returns:
            bool: True si se registró correctamente, False si el ID ya existe.
        """
        if usuario.id_usuario in self._ids_usuarios:
            print(f" "
                  f" Ya existe un usuario con ID '{usuario.id_usuario}'.")
            return False

        # Agregar ID al conjunto (O(1)) para garantizar unicidad
        self._ids_usuarios.add(usuario.id_usuario)
        # Almacenar usuario en diccionario para acceso eficiente
        self._usuarios[usuario.id_usuario] = usuario
        print(f" "
              f" Usuario '{usuario.nombre}' (ID: {usuario.id_usuario}) registrado exitosamente.")
        return True

    def dar_de_baja_usuario(self, id_usuario: str) -> Usuario | None:
        """
        Da de baja a un usuario de la biblioteca.

        Verifica que el usuario no tenga libros prestados antes de darlo de baja.

        Args:
            id_usuario (str): El ID del usuario a dar de baja.

        Returns:
            Usuario | None: El usuario dado de baja, o None si no se pudo.
        """
        if id_usuario not in self._ids_usuarios:
            print(f" "
                  f" No se encontró un usuario con ID '{id_usuario}'.")
            return None

        usuario = self._usuarios[id_usuario]

        # Verificar que no tenga libros prestados
        if usuario.cantidad_libros_prestados > 0:
            print(f" "
                  f" No se puede dar de baja a '{usuario.nombre}' porque tiene "
                  f"{usuario.cantidad_libros_prestados} libro(s) prestado(s).")
            print("       Debe devolver todos los libros antes de darse de baja.")
            return None

        # Eliminar del conjunto de IDs (O(1))
        self._ids_usuarios.discard(id_usuario)
        # Eliminar del diccionario de usuarios
        del self._usuarios[id_usuario]
        print(f" "
              f" Usuario '{usuario.nombre}' (ID: {id_usuario}) dado de baja exitosamente.")
        return usuario

    # =========================================================================
    # PRÉSTAMOS Y DEVOLUCIONES
    # =========================================================================

    def prestar_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Presta un libro a un usuario.

        Verifica que el libro exista, esté disponible y que el usuario esté registrado.

        Args:
            isbn (str): El ISBN del libro a prestar.
            id_usuario (str): El ID del usuario que solicita el préstamo.

        Returns:
            bool: True si el préstamo fue exitoso, False en caso contrario.
        """
        # Validar que el libro existe en el catálogo
        if isbn not in self._catalogo:
            print(f" "
                  f" No se encontró un libro con ISBN '{isbn}' en el catálogo.")
            return False

        # Validar que el usuario esté registrado (búsqueda O(1) en el conjunto)
        if id_usuario not in self._ids_usuarios:
            print(f" "
                  f" No se encontró un usuario con ID '{id_usuario}'.")
            return False

        libro = self._catalogo[isbn]
        usuario = self._usuarios[id_usuario]

        # Verificar disponibilidad del libro
        if not libro.disponible:
            print(f" "
                  f" El libro '{libro.titulo}' no está disponible (ya está prestado).")
            return False

        # Realizar el préstamo
        if usuario.agregar_libro_prestado(libro):
            libro.disponible = False
            # Registrar en el historial
            self._historial_prestamos.append({
                "tipo": "préstamo",
                "isbn": isbn,
                "titulo": libro.titulo,
                "id_usuario": id_usuario,
                "nombre_usuario": usuario.nombre
            })
            print(f" "
                  f" Libro '{libro.titulo}' prestado a '{usuario.nombre}' exitosamente.")
            return True

        return False

    def devolver_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Registra la devolución de un libro por parte de un usuario.

        Args:
            isbn (str): El ISBN del libro a devolver.
            id_usuario (str): El ID del usuario que devuelve el libro.

        Returns:
            bool: True si la devolución fue exitosa, False en caso contrario.
        """
        # Validar que el libro existe
        if isbn not in self._catalogo:
            print(f" "
                  f" No se encontró un libro con ISBN '{isbn}' en el catálogo.")
            return False

        # Validar que el usuario existe
        if id_usuario not in self._ids_usuarios:
            print(f" "
                  f" No se encontró un usuario con ID '{id_usuario}'.")
            return False

        libro = self._catalogo[isbn]
        usuario = self._usuarios[id_usuario]

        # Intentar eliminar el libro de la lista del usuario
        libro_devuelto = usuario.eliminar_libro_prestado(isbn)
        if libro_devuelto:
            libro.disponible = True
            # Registrar en el historial
            self._historial_prestamos.append({
                "tipo": "devolución",
                "isbn": isbn,
                "titulo": libro.titulo,
                "id_usuario": id_usuario,
                "nombre_usuario": usuario.nombre
            })
            print(f" "
                  f" Libro '{libro.titulo}' devuelto por '{usuario.nombre}' exitosamente.")
            return True

        return False

    # =========================================================================
    # BÚSQUEDAS
    # =========================================================================

    def buscar_por_titulo(self, titulo: str) -> list[Libro]:
        """
        Busca libros por título (búsqueda parcial, insensible a mayúsculas).

        Args:
            titulo (str): El título o fragmento de título a buscar.

        Returns:
            list[Libro]: Lista de libros que coinciden con la búsqueda.
        """
        resultados = [
            libro for libro in self._catalogo.values()
            if titulo.lower() in libro.titulo.lower()
        ]

        if not resultados:
            print(f"  🔍 No se encontraron libros con título que contenga '{titulo}'.")
        else:
            print(f"  🔍 Se encontraron {len(resultados)} libro(s) con título que contiene '{titulo}':")
            for libro in resultados:
                print(f"      {libro}")

        return resultados

    def buscar_por_autor(self, autor: str) -> list[Libro]:
        """
        Busca libros por autor (búsqueda parcial, insensible a mayúsculas).

        Args:
            autor (str): El nombre del autor o fragmento a buscar.

        Returns:
            list[Libro]: Lista de libros que coinciden con la búsqueda.
        """
        resultados = [
            libro for libro in self._catalogo.values()
            if autor.lower() in libro.autor.lower()
        ]

        if not resultados:
            print(f"  🔍 No se encontraron libros del autor '{autor}'.")
        else:
            print(f"  🔍 Se encontraron {len(resultados)} libro(s) del autor '{autor}':")
            for libro in resultados:
                print(f"      {libro}")

        return resultados

    def buscar_por_categoria(self, categoria: str) -> list[Libro]:
        """
        Busca libros por categoría (búsqueda parcial, insensible a mayúsculas).

        Args:
            categoria (str): La categoría o fragmento a buscar.

        Returns:
            list[Libro]: Lista de libros que coinciden con la búsqueda.
        """
        resultados = [
            libro for libro in self._catalogo.values()
            if categoria.lower() in libro.categoria.lower()
        ]

        if not resultados:
            print(f"  🔍 No se encontraron libros en la categoría '{categoria}'.")
        else:
            print(f"  🔍 Se encontraron {len(resultados)} libro(s) en la categoría '{categoria}':")
            for libro in resultados:
                print(f"      {libro}")

        return resultados

    # =========================================================================
    # LISTADOS E INFORMES
    # =========================================================================

    def listar_libros_usuario(self, id_usuario: str) -> list[Libro]:

        if id_usuario not in self._ids_usuarios:
            print(f" "
                  f" No se encontró un usuario con ID '{id_usuario}'.")
            return []

        usuario = self._usuarios[id_usuario]
        libros = usuario.libros_prestados

        if not libros:
            print(f"  📋 El usuario '{usuario.nombre}' no tiene libros prestados actualmente.")
        else:
            print(f"  📋 Libros prestados a '{usuario.nombre}' ({len(libros)}):")
            for i, libro in enumerate(libros, 1):
                print(f"      {i}. {libro}")

        return libros

    def listar_catalogo(self):
        """Muestra todos los libros del catálogo de la biblioteca."""
        if not self._catalogo:
            print(f"  📚 El catálogo de '{self._nombre}' está vacío.")
            return

        print(f"  📚 Catálogo de '{self._nombre}' ({self.total_libros} libros):")
        for i, libro in enumerate(self._catalogo.values(), 1):
            print(f"      {i}. {libro}")

    def listar_usuarios(self):
        """Muestra todos los usuarios registrados en la biblioteca."""
        if not self._usuarios:
            print(f"  👥 No hay usuarios registrados en '{self._nombre}'.")
            return

        print(f"  👥 Usuarios registrados en '{self._nombre}' ({self.total_usuarios}):")
        for i, usuario in enumerate(self._usuarios.values(), 1):
            print(f"      {i}. {usuario}")

    def mostrar_historial(self):
        """Muestra el historial completo de préstamos y devoluciones."""
        if not self._historial_prestamos:
            print("  📜 No hay registros en el historial de préstamos.")
            return

        print(f"  📜 Historial de préstamos y devoluciones ({len(self._historial_prestamos)} registros):")
        for i, registro in enumerate(self._historial_prestamos, 1):
            tipo = "📤 Préstamo" if registro["tipo"] == "préstamo" else "📥 Devolución"
            print(f"      {i}. {tipo}: '{registro['titulo']}' (ISBN: {registro['isbn']}) "
                  f"— Usuario: {registro['nombre_usuario']} (ID: {registro['id_usuario']})")

    def mostrar_estadisticas(self):
        """Muestra estadísticas generales de la biblioteca."""
        print(f"\n  📊 Estadísticas de '{self._nombre}':")
        print(f"      Total de libros en catálogo: {self.total_libros}")
        print(f"      Libros disponibles: {self.libros_disponibles}")
        print(f"      Libros prestados: {self.total_libros - self.libros_disponibles}")
        print(f"      Usuarios registrados: {self.total_usuarios}")
        print(f"      Total de operaciones en historial: {len(self._historial_prestamos)}")

    # --- Métodos especiales ---

    def __str__(self) -> str:
        """Representación en cadena de la biblioteca."""
        return (f"🏛️  Biblioteca '{self._nombre}' | "
                f"Libros: {self.total_libros} | Usuarios: {self.total_usuarios}")

    def __repr__(self) -> str:
        """Representación técnica de la biblioteca."""
        return f"Biblioteca(nombre='{self._nombre}')"

