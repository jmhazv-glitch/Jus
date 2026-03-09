"""
Sistema de Gestión de Biblioteca Digital - Script Principal

Este script demuestra todas las funcionalidades del sistema:
1. Creación de libros con tuplas inmutables (autor, título)
2. Registro de usuarios con IDs únicos (conjunto/set)
3. Gestión del catálogo con diccionario ISBN → Libro
4. Préstamos y devoluciones de libros
5. Búsquedas por título, autor y categoría
6. Listados e historial de operaciones
"""
from libro import Libro
from usuario import Usuario
from biblioteca import Biblioteca

def separador(titulo: str):
    """Imprime un separador visual con un título de sección."""
    print(f"\n{'=' * 70}")
    print(f"  {titulo}")
    print(f"{'=' * 70}")

def main():
    """Función principal que ejecuta las pruebas del sistema."""

    print("\n"  + " SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL "  + "\n")

    # 1. CREAR LA BIBLIOTECA
    separador("1. CREACIÓN DE LA BIBLIOTECA")

    biblioteca = Biblioteca("Biblioteca Central Digital")
    print(f"  {biblioteca}")

    # 2. CREAR LIBROS (usando tuplas inmutables para autor, título)
    separador("2. CREACIÓN DE LIBROS")

    # Crear instancias de libros con diferentes categorías
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Ficción", "978-0-06-088328-7")
    libro2 = Libro("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", "978-84-376-0494-7")
    libro3 = Libro("El Principito", "Antoine de Saint-Exupéry", "Ficción", "978-0-15-601219-5")
    libro4 = Libro("Breve Historia del Tiempo", "Stephen Hawking", "Ciencia", "978-0-553-38016-3")
    libro5 = Libro("1984", "George Orwell", "Ficción", "978-0-451-52493-5")
    libro6 = Libro("Cosmos", "Carl Sagan", "Ciencia", "978-0-345-53943-4")
    libro7 = Libro("La Casa de los Espíritus", "Isabel Allende", "Ficción", "978-0-553-38380-5")
    libro8 = Libro("El Alquimista", "Paulo Coelho", "Ficción", "978-0-06-112008-4")

    # Mostrar la tupla inmutable (autor, título) de algunos libros
    print(f"  Tupla inmutable de libro1: {libro1.info_libro}")
    print(f"  Tupla inmutable de libro2: {libro2.info_libro}")
    print(f"  Tupla inmutable de libro4: {libro4.info_libro}")
    print(f"\n  Detalle de libros creados:")
    for libro in [libro1, libro2, libro3, libro4, libro5, libro6, libro7, libro8]:
        print(f"    {libro}")

    # 3. AGREGAR LIBROS AL CATÁLOGO
    separador("3. AGREGAR LIBROS AL CATÁLOGO (Diccionario ISBN → Libro)")

    libros = [libro1, libro2, libro3, libro4, libro5, libro6, libro7, libro8]
    for libro in libros:
        biblioteca.agregar_libro(libro)

    # Intentar agregar un libro duplicado (mismo ISBN)
    print("\n  --- Intentando agregar un libro con ISBN duplicado ---")
    libro_duplicado = Libro("Libro Duplicado", "Autor Desconocido", "Test", "978-0-06-088328-7")
    biblioteca.agregar_libro(libro_duplicado)

    # Mostrar catálogo completo
    print()
    biblioteca.listar_catalogo()

    # 4. REGISTRAR USUARIOS (usando conjunto para IDs únicos)
    separador("4. REGISTRO DE USUARIOS (Conjunto de IDs únicos)")

    usuario1 = Usuario("Ana López", "USR-001")
    usuario2 = Usuario("Carlos Rodríguez", "USR-002")
    usuario3 = Usuario("María García", "USR-003")
    usuario4 = Usuario("Pedro Martínez", "USR-004")

    for usuario in [usuario1, usuario2, usuario3, usuario4]:
        biblioteca.registrar_usuario(usuario)

    # Intentar registrar un usuario con ID duplicado
    print("\n  --- Intentando registrar un usuario con ID duplicado ---")
    usuario_duplicado = Usuario("Juan Pérez", "USR-001")
    biblioteca.registrar_usuario(usuario_duplicado)

    # Listar usuarios
    print()
    biblioteca.listar_usuarios()

    # 5. PRÉSTAMOS DE LIBROS

    separador("5. PRÉSTAMOS DE LIBROS")

    # Realizar préstamos exitosos
    biblioteca.prestar_libro("978-0-06-088328-7", "USR-001")  # Ana ← Cien Años de Soledad
    biblioteca.prestar_libro("978-0-15-601219-5", "USR-001")  # Ana ← El Principito
    biblioteca.prestar_libro("978-84-376-0494-7", "USR-002")  # Carlos ← Don Quijote
    biblioteca.prestar_libro("978-0-553-38016-3", "USR-003")  # María ← Breve Historia del Tiempo
    biblioteca.prestar_libro("978-0-451-52493-5", "USR-003")  # María ← 1984

    # Intentar prestar un libro que ya está prestado
    print("\n  --- Intentando prestar un libro que ya está prestado ---")
    biblioteca.prestar_libro("978-0-06-088328-7", "USR-004")  # Cien Años ya está prestado

    # Intentar prestar a un usuario inexistente
    print("\n  --- Intentando prestar a un usuario inexistente ---")
    biblioteca.prestar_libro("978-0-345-53943-4", "USR-999")

    # Intentar prestar un libro inexistente
    print("\n  --- Intentando prestar un libro inexistente ---")
    biblioteca.prestar_libro("000-0-000-00000-0", "USR-001")

    # 6. LISTAR LIBROS PRESTADOS POR USUARIO

    separador("6. LIBROS PRESTADOS POR USUARIO")

    biblioteca.listar_libros_usuario("USR-001")
    print()
    biblioteca.listar_libros_usuario("USR-002")
    print()
    biblioteca.listar_libros_usuario("USR-003")
    print()
    biblioteca.listar_libros_usuario("USR-004")

    # 7. BÚSQUEDAS DE LIBROS

    separador("7. BÚSQUEDAS DE LIBROS")

    # Buscar por título
    print("\n  --- Búsqueda por título: 'el' ---")
    biblioteca.buscar_por_titulo("el")

    # Buscar por autor
    print("\n  --- Búsqueda por autor: 'García' ---")
    biblioteca.buscar_por_autor("García")

    # Buscar por categoría
    print("\n  --- Búsqueda por categoría: 'Ciencia' ---")
    biblioteca.buscar_por_categoria("Ciencia")

    # Buscar por categoría: Ficción
    print("\n  --- Búsqueda por categoría: 'Ficción' ---")
    biblioteca.buscar_por_categoria("Ficción")

    # Búsqueda sin resultados
    print("\n  --- Búsqueda por título: 'Python' ---")
    biblioteca.buscar_por_titulo("Python")

    # 8. DEVOLUCIÓN DE LIBROS

    separador("8. DEVOLUCIÓN DE LIBROS")

    biblioteca.devolver_libro("978-0-06-088328-7", "USR-001")  # Ana devuelve Cien Años
    biblioteca.devolver_libro("978-84-376-0494-7", "USR-002")  # Carlos devuelve Don Quijote

    # Intentar devolver un libro que el usuario no tiene
    print("\n  --- Intentando devolver un libro que el usuario no tiene ---")
    biblioteca.devolver_libro("978-0-345-53943-4", "USR-001")

    # Verificar libros de Ana después de la devolución
    print()
    biblioteca.listar_libros_usuario("USR-001")

    # 9. ELIMINAR LIBROS DEL CATÁLOGO

    separador("9. ELIMINAR LIBROS DEL CATÁLOGO")

    # Eliminar un libro disponible
    biblioteca.eliminar_libro("978-0-553-38380-5")  # Eliminar La Casa de los Espíritus

    # Intentar eliminar un libro prestado
    print("\n  --- Intentando eliminar un libro que está prestado ---")
    biblioteca.eliminar_libro("978-0-451-52493-5")  # 1984 está prestado por María

    # Intentar eliminar un libro que no existe
    print("\n  --- Intentando eliminar un libro que no existe ---")
    biblioteca.eliminar_libro("000-0-000-00000-0")


    # 10. DAR DE BAJA USUARIOS

    separador("10. DAR DE BAJA USUARIOS")

    # Dar de baja a un usuario sin libros prestados (Carlos ya devolvió su libro)
    biblioteca.dar_de_baja_usuario("USR-002")

    # Intentar dar de baja a un usuario con libros prestados
    print("\n  --- Intentando dar de baja a un usuario con libros prestados ---")
    biblioteca.dar_de_baja_usuario("USR-003")  # María tiene libros prestados

    # Intentar dar de baja a un usuario inexistente
    print("\n  --- Intentando dar de baja a un usuario inexistente ---")
    biblioteca.dar_de_baja_usuario("USR-999")

    # 11. HISTORIAL Y ESTADÍSTICAS

    separador("11. HISTORIAL DE PRÉSTAMOS Y DEVOLUCIONES")

    biblioteca.mostrar_historial()

    separador("12. ESTADÍSTICAS FINALES")

    biblioteca.mostrar_estadisticas()

    # Mostrar catálogo actualizado
    print()
    biblioteca.listar_catalogo()
    print()
    biblioteca.listar_usuarios()

    # 13. DEMOSTRACIÓN DE ESTRUCTURAS DE DATOS

    separador("13. DEMOSTRACIÓN DE ESTRUCTURAS DE DATOS UTILIZADAS")

    print("\n  📌 TUPLA (inmutable) — Información del libro:")
    print(f"     libro1.info_libro = {libro1.info_libro}")
    print(f"     Tipo: {type(libro1.info_libro)}")
    print(f"     Autor (desde tupla): {libro1.info_libro[0]}")
    print(f"     Título (desde tupla): {libro1.info_libro[1]}")

    print("\n  📌 DICCIONARIO — Catálogo de libros (ISBN → Libro):")
    print(f"     Tipo del catálogo: dict")
    print(f"     Cantidad de entradas: {biblioteca.total_libros}")
    print(f"     Ejemplo de acceso O(1) por ISBN: buscar '978-0-553-38016-3'")
    resultado = biblioteca.buscar_por_titulo("Breve Historia")

    print("\n  📌 CONJUNTO (set) — IDs de usuarios únicos:")
    print(f"     Tipo: set")
    print(f"     Garantiza que no haya IDs duplicados")
    print(f"     Verificación de pertenencia en O(1)")

    print("\n  📌 LISTA — Libros prestados por usuario:")
    print(f"     usuario1.libros_prestados = {usuario1.libros_prestados}")
    print(f"     Tipo: {type(usuario1.libros_prestados)}")
    print(f"     Permite agregar/eliminar dinámicamente")

    print(f"\n{'=' * 70}")
    print("   FIN DE LA DEMOSTRACIÓN DEL SISTEMA DE BIBLIOTECA DIGITAL ")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()

