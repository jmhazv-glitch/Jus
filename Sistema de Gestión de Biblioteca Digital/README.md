# 📚 Sistema de Gestión de Biblioteca Digital

## Descripción

Sistema completo de gestión de biblioteca digital desarrollado en Python utilizando **Programación Orientada a Objetos (POO)**. Permite administrar libros, usuarios registrados, préstamos y devoluciones de forma eficiente.

## Estructura del Proyecto

```
Sistema de Gestión de Biblioteca Digital/
├── libro.py         # Clase Libro
├── usuario.py       # Clase Usuario
├── biblioteca.py    # Clase Biblioteca (gestión central)
├── main.py          # Script principal de demostración
└── README.md        # Documentación del proyecto
```

## Clases Principales

### 📖 `Libro` (`libro.py`)
Representa un libro en la biblioteca digital.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `info_libro` | `tuple` | Tupla inmutable `(autor, título)` |
| `categoria` | `str` | Categoría/género del libro |
| `isbn` | `str` | Código ISBN único |
| `disponible` | `bool` | Disponibilidad para préstamo |

**¿Por qué tupla?** Se usa una tupla `(autor, título)` porque estos atributos son **inmutables** una vez creado el libro, garantizando integridad de datos.

### 👤 `Usuario` (`usuario.py`)
Representa a un usuario registrado en la biblioteca.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `nombre` | `str` | Nombre completo |
| `id_usuario` | `str` | Identificador único |
| `libros_prestados` | `list[Libro]` | Libros actualmente prestados |

**¿Por qué lista?** Se usa una lista para `libros_prestados` porque permite agregar y eliminar libros **dinámicamente** según los préstamos y devoluciones.

### 🏛️ `Biblioteca` (`biblioteca.py`)
Gestiona la colección completa de libros, usuarios y préstamos.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `catalogo` | `dict[str, Libro]` | ISBN → Libro (acceso O(1)) |
| `ids_usuarios` | `set[str]` | Conjunto de IDs únicos |
| `usuarios` | `dict[str, Usuario]` | ID → Usuario |
| `historial_prestamos` | `list[dict]` | Registro de operaciones |

**¿Por qué diccionario?** El catálogo usa un `dict` con ISBN como clave para **búsquedas en O(1)**, evitando recorrer toda la colección.

**¿Por qué conjunto (set)?** Los IDs de usuarios se almacenan en un `set` para **garantizar unicidad** y verificar pertenencia en O(1).

## Estructuras de Datos Utilizadas

| Estructura | Uso | Justificación |
|------------|-----|---------------|
| **Tupla** | `(autor, título)` en `Libro` | Datos inmutables que no cambian |
| **Lista** | Libros prestados en `Usuario` | Colección dinámica modificable |
| **Diccionario** | Catálogo `{ISBN: Libro}` | Acceso O(1) por clave |
| **Conjunto** | IDs de usuarios `{id1, id2, ...}` | Unicidad garantizada, búsqueda O(1) |

## Funcionalidades

- ✅ **Agregar/Eliminar libros** del catálogo
- ✅ **Registrar/Dar de baja usuarios** con validación de unicidad
- ✅ **Prestar/Devolver libros** con validaciones completas
- ✅ **Buscar libros** por título, autor o categoría (búsqueda parcial)
- ✅ **Listar libros prestados** por usuario
- ✅ **Historial de operaciones** (préstamos y devoluciones)
- ✅ **Estadísticas** de la biblioteca

## Ejecución

```bash
cd "Sistema de Gestión de Biblioteca Digital"
python main.py
```

## Ejemplo de Uso

```python
from libro import Libro
from usuario import Usuario
from biblioteca import Biblioteca

# Crear biblioteca
biblioteca = Biblioteca("Mi Biblioteca")

# Crear y agregar un libro (tupla inmutable para autor y título)
libro = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Ficción", "978-0-06-088328-7")
biblioteca.agregar_libro(libro)

# Registrar un usuario (ID único verificado con set)
usuario = Usuario("Ana López", "USR-001")
biblioteca.registrar_usuario(usuario)

# Prestar un libro
biblioteca.prestar_libro("978-0-06-088328-7", "USR-001")

# Buscar libros por categoría
biblioteca.buscar_por_categoria("Ficción")

# Devolver un libro
biblioteca.devolver_libro("978-0-06-088328-7", "USR-001")
```

## Autor

Proyecto desarrollado como ejercicio de Programación Orientada a Objetos en Python.

