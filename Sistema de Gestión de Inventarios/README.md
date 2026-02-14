# Sistema de Gestión de Inventarios

## Descripción
Sistema de gestión de inventarios simple y eficiente para tiendas, desarrollado en Python. Permite administrar productos mediante operaciones CRUD (Crear, Leer, Actualizar, Eliminar) con una interfaz interactiva de consola.

## Características

- ✅ Añadir nuevos productos con ID único
- ✅ Eliminar productos por ID
- ✅ Actualizar cantidad y precio de productos
- ✅ Buscar productos por nombre (búsqueda parcial)
- ✅ Buscar productos por ID
- ✅ Visualizar todos los productos del inventario
- ✅ Estadísticas del inventario (valor total, productos más caros/baratos, etc.)
- ✅ Validación de entradas del usuario
- ✅ Interfaz amigable con emojis y formato claro

## Estructura del Proyecto

```
inventario-sistema/
│
├── producto.py          # Clase Producto con atributos y métodos
├── inventario.py        # Clase Inventario para gestión de productos
├── main.py             # Interfaz de usuario y menú interactivo
├── test_sistema.py     # Pruebas automatizadas del sistema
├── README.md           # Documentación del proyecto
├── .gitignore          # Archivos a ignorar en Git
└── requirements.txt    # Dependencias del proyecto
```

## Instalación y Uso

### Requisitos Previos
- Python 3.7 o superior
- PyCharm (recomendado) o cualquier IDE de Python

### Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/inventario-sistema.git
   cd inventario-sistema
   ```

2. **Ejecutar el programa:**
   ```bash
   python main.py
   ```

### Uso desde PyCharm

1. Abrir PyCharm
2. Seleccionar `File > Open` y navegar a la carpeta del proyecto
3. Hacer clic derecho en `main.py`
4. Seleccionar `Run 'main'`

##Guía de Uso

### Menú Principal

El sistema presenta un menú con las siguientes opciones:

1. **Añadir nuevo producto**: Crear un producto con ID, nombre, cantidad y precio
2. **Eliminar producto**: Eliminar un producto existente por su ID
3. **Actualizar cantidad**: Modificar la cantidad en stock de un producto
4. **Actualizar precio**: Modificar el precio de un producto
5. **Buscar por nombre**: Buscar productos que contengan el texto ingresado
6. **Buscar por ID**: Buscar un producto específico por su ID
7. **Mostrar todos**: Listar todos los productos en el inventario
8. **Estadísticas**: Ver resumen y análisis del inventario
9. **Salir**: Cerrar el programa

### Ejemplo de Uso

```
=============================================================
          SISTEMA DE GESTIÓN DE INVENTARIOS          
=============================================================

1. Añadir nuevo producto
2. Eliminar producto
...

Seleccione una opción (1-9): 1

--- AÑADIR NUEVO PRODUCTO ---
Ingrese el ID del producto: 101
Ingrese el nombre del producto: Auriculares Bluetooth
Ingrese la cantidad: 25
Ingrese el precio: $49.99

Producto 'Auriculares Bluetooth' agregado exitosamente!
```

## Pruebas

El proyecto incluye un archivo `test_sistema.py` con pruebas automatizadas para verificar la funcionalidad del sistema.

Para ejecutar las pruebas:
```bash
python test_sistema.py
```

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **POO (Programación Orientada a Objetos)**: Diseño modular con clases
- **Encapsulamiento**: Atributos privados con getters y setters

## Características Técnicas

### Clase Producto
- Encapsulamiento de datos con atributos privados
- Getters y setters para todos los atributos
- Métodos `__str__` y `__repr__` para representación

### Clase Inventario
- Gestión de lista de productos
- Validación de IDs únicos
- Búsqueda flexible (por ID y por nombre)
- Cálculo de estadísticas

### Validaciones
- Verificación de tipos de datos
- Validación de valores positivos
- Prevención de IDs duplicados
- Confirmación para operaciones críticas
