"""
Módulo test_sistema.py
Pruebas automatizadas para el Sistema de Gestión de Inventarios.
Incluye pruebas de persistencia en archivos y manejo de excepciones.
"""

from producto import Producto
from inventario import Inventario
import os
import tempfile

def test_crear_producto():
    """Prueba la creación de un producto."""
    print("\n Test 1: Crear Producto")
    producto = Producto(1, "Laptop", 10, 999.99)
    
    assert producto.get_id() == 1, "Error en ID"
    assert producto.get_nombre() == "Laptop", "Error en nombre"
    assert producto.get_cantidad() == 10, "Error en cantidad"
    assert producto.get_precio() == 999.99, "Error en precio"
    
    print("Test 1 PASADO: Producto creado correctamente")

def test_getters_setters():
    """Prueba los getters y setters de Producto."""
    print("\nTest 2: Getters y Setters")
    producto = Producto(1, "Mouse", 5, 25.00)
    
    # Probar setters
    producto.set_id(2)
    producto.set_nombre("Teclado")
    producto.set_cantidad(15)
    producto.set_precio(50.00)
    
    # Verificar con getters
    assert producto.get_id() == 2, "Error en set_id"
    assert producto.get_nombre() == "Teclado", "Error en set_nombre"
    assert producto.get_cantidad() == 15, "Error en set_cantidad"
    assert producto.get_precio() == 50.00, "Error en set_precio"
    
    print("Test 2 PASADO: Getters y setters funcionan correctamente")

def test_agregar_producto():
    """Prueba agregar productos al inventario."""
    print("\n Test 3: Agregar Producto al Inventario")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)
        producto1 = Producto(1, "Monitor", 20, 299.99)
        producto2 = Producto(2, "Webcam", 30, 79.99)

        # Agregar productos - ahora retorna tupla (exito, mensaje)
        exito1, _ = inventario.agregar_producto(producto1)
        exito2, _ = inventario.agregar_producto(producto2)
        assert exito1 == True, "Error al agregar producto1"
        assert exito2 == True, "Error al agregar producto2"

        # Intentar agregar producto con ID duplicado
        producto_duplicado = Producto(1, "Otro producto", 5, 10.00)
        exito_dup, _ = inventario.agregar_producto(producto_duplicado)
        assert exito_dup == False, "No se detectó ID duplicado"

        assert inventario.obtener_total_productos() == 2, "Error en cantidad de productos"

        print("Test 3 PASADO: Productos agregados correctamente")
    finally:
        # Limpiar archivo temporal
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_eliminar_producto():
    """Prueba eliminar productos del inventario."""
    print("\nTest 4: Eliminar Producto")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)
        producto = Producto(1, "Auriculares", 40, 59.99)

        inventario.agregar_producto(producto)
        assert inventario.obtener_total_productos() == 1, "Error al verificar cantidad inicial"

        # Eliminar producto existente - ahora retorna tupla (exito, mensaje)
        exito, _ = inventario.eliminar_producto(1)
        assert exito == True, "Error al eliminar producto existente"
        assert inventario.obtener_total_productos() == 0, "Error al verificar cantidad después de eliminar"

        # Intentar eliminar producto inexistente
        exito_no, _ = inventario.eliminar_producto(999)
        assert exito_no == False, "No se detectó producto inexistente"

        print("Test 4 PASADO: Producto eliminado correctamente")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_actualizar_cantidad():
    """Prueba actualizar la cantidad de un producto."""
    print("\nTest 5: Actualizar Cantidad")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)
        producto = Producto(1, "Cable USB", 100, 9.99)

        inventario.agregar_producto(producto)

        # Actualizar cantidad - ahora retorna tupla (exito, mensaje)
        exito, _ = inventario.actualizar_cantidad(1, 150)
        assert exito == True, "Error al actualizar cantidad"
        assert producto.get_cantidad() == 150, "Cantidad no actualizada correctamente"

        # Intentar actualizar producto inexistente
        exito_no, _ = inventario.actualizar_cantidad(999, 100)
        assert exito_no == False, "No se detectó producto inexistente"

        print("Test 5 PASADO: Cantidad actualizada correctamente")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_actualizar_precio():
    """Prueba actualizar el precio de un producto."""
    print("\nTest 6: Actualizar Precio")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)
        producto = Producto(1, "SSD 1TB", 25, 149.99)

        inventario.agregar_producto(producto)

        # Actualizar precio - ahora retorna tupla (exito, mensaje)
        exito, _ = inventario.actualizar_precio(1, 129.99)
        assert exito == True, "Error al actualizar precio"
        assert producto.get_precio() == 129.99, "Precio no actualizado correctamente"

        # Intentar actualizar producto inexistente
        exito_no, _ = inventario.actualizar_precio(999, 100.00)
        assert exito_no == False, "No se detectó producto inexistente"

        print("Test 6 PASADO: Precio actualizado correctamente")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_buscar_por_nombre():
    """Prueba la búsqueda de productos por nombre."""
    print("\nTest 7: Buscar por Nombre")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)

        inventario.agregar_producto(Producto(1, "Laptop HP", 10, 899.99))
        inventario.agregar_producto(Producto(2, "Laptop Dell", 15, 999.99))
        inventario.agregar_producto(Producto(3, "Mouse", 50, 25.00))

        # Buscar "Laptop" debe encontrar 2 productos
        resultados = inventario.buscar_por_nombre("Laptop")
        assert len(resultados) == 2, f"Esperaba 2 resultados, obtuvo {len(resultados)}"

        # Buscar "Mouse" debe encontrar 1 producto
        resultados = inventario.buscar_por_nombre("Mouse")
        assert len(resultados) == 1, f"Esperaba 1 resultado, obtuvo {len(resultados)}"

        # Buscar algo inexistente
        resultados = inventario.buscar_por_nombre("Tablet")
        assert len(resultados) == 0, f"Esperaba 0 resultados, obtuvo {len(resultados)}"

        # Búsqueda case-insensitive
        resultados = inventario.buscar_por_nombre("laptop")
        assert len(resultados) == 2, "Error en búsqueda case-insensitive"

        print("Test 7 PASADO: Búsqueda por nombre funciona correctamente")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_buscar_por_id():
    """Prueba la búsqueda de productos por ID."""
    print("\nTest 8: Buscar por ID")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)

        producto = Producto(100, "Impresora", 8, 299.99)
        inventario.agregar_producto(producto)

        # Buscar producto existente
        encontrado = inventario.buscar_por_id(100)
        assert encontrado is not None, "No se encontró el producto"
        assert encontrado.get_nombre() == "Impresora", "Producto incorrecto encontrado"

        # Buscar producto inexistente
        no_encontrado = inventario.buscar_por_id(999)
        assert no_encontrado is None, "Se encontró un producto que no debería existir"

        print("Test 8 PASADO: Búsqueda por ID funciona correctamente")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_mostrar_todos():
    """Prueba obtener todos los productos."""
    print("\nTest 9: Mostrar Todos los Productos")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)

        # Inventario vacío
        productos = inventario.mostrar_todos()
        assert len(productos) == 0, "Inventario debería estar vacío"

        # Agregar productos
        inventario.agregar_producto(Producto(1, "Producto 1", 10, 10.00))
        inventario.agregar_producto(Producto(2, "Producto 2", 20, 20.00))
        inventario.agregar_producto(Producto(3, "Producto 3", 30, 30.00))

        productos = inventario.mostrar_todos()
        assert len(productos) == 3, f"Esperaba 3 productos, obtuvo {len(productos)}"

        print("Test 9 PASADO: Mostrar todos los productos funciona correctamente")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_valor_total_inventario():
    """Prueba el cálculo del valor total del inventario."""
    print("\nTest 10: Valor Total del Inventario")
    # Usar archivo temporal para las pruebas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        inventario = Inventario(archivo_temp)

        # Agregar productos con valores conocidos
        # Producto 1: 10 unidades x $100 = $1000
        # Producto 2: 20 unidades x $50 = $1000
        # Total esperado: $2000
        inventario.agregar_producto(Producto(1, "Producto A", 10, 100.00))
        inventario.agregar_producto(Producto(2, "Producto B", 20, 50.00))

        valor_total = inventario.obtener_valor_total_inventario()
        assert valor_total == 2000.00, f"Esperaba $2000, obtuvo ${valor_total}"

        print("Test 10 PASADO: Cálculo de valor total correcto")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)

def test_str_representation():
    """Prueba la representación en string de Producto."""
    print("\nTest 11: Representación String")
    producto = Producto(1, "Test Product", 5, 49.99)
    
    str_repr = str(producto)
    assert "ID: 1" in str_repr, "ID no aparece en string"
    assert "Test Product" in str_repr, "Nombre no aparece en string"
    assert "5" in str_repr, "Cantidad no aparece en string"
    assert "49.99" in str_repr, "Precio no aparece en string"
    
    print("Test 11 PASADO: Representación string correcta")


# =====================================================
# NUEVAS PRUEBAS DE PERSISTENCIA EN ARCHIVOS
# =====================================================

def test_producto_to_line():
    """Prueba la serialización de un producto a línea de texto."""
    print("\nTest 12: Serialización de Producto (to_line)")
    producto = Producto(1, "Laptop HP", 10, 899.99)

    linea = producto.to_line()
    assert linea == "1|Laptop HP|10|899.99", f"Error en serialización: {linea}"

    print("Test 12 PASADO: Serialización de producto correcta")


def test_producto_from_line():
    """Prueba la deserialización de una línea de texto a producto."""
    print("\nTest 13: Deserialización de Producto (from_line)")

    # Línea válida
    linea = "1|Monitor Samsung|15|299.99"
    producto = Producto.from_line(linea)

    assert producto.get_id() == 1, "Error en ID deserializado"
    assert producto.get_nombre() == "Monitor Samsung", "Error en nombre deserializado"
    assert producto.get_cantidad() == 15, "Error en cantidad deserializada"
    assert producto.get_precio() == 299.99, "Error en precio deserializado"

    # Línea inválida (menos campos)
    try:
        Producto.from_line("1|Monitor|15")
        assert False, "Debería lanzar ValueError para línea incompleta"
    except ValueError:
        pass  # Comportamiento esperado

    # Línea con tipo de dato inválido
    try:
        Producto.from_line("abc|Monitor|15|299.99")
        assert False, "Debería lanzar ValueError para ID no numérico"
    except ValueError:
        pass  # Comportamiento esperado

    print("Test 13 PASADO: Deserialización de producto correcta")


def test_persistencia_archivo():
    """Prueba que los datos persisten correctamente en archivo."""
    print("\nTest 14: Persistencia en Archivo")

    # Crear archivo temporal para la prueba
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        # Crear inventario y agregar productos
        inventario1 = Inventario(archivo_temp)
        inventario1.agregar_producto(Producto(1, "Producto A", 10, 100.00))
        inventario1.agregar_producto(Producto(2, "Producto B", 20, 200.00))

        # Crear nuevo inventario que lee del mismo archivo
        inventario2 = Inventario(archivo_temp)

        # Verificar que los productos se cargaron
        assert inventario2.obtener_total_productos() == 2, "No se cargaron los productos"

        producto1 = inventario2.buscar_por_id(1)
        assert producto1 is not None, "Producto 1 no encontrado"
        assert producto1.get_nombre() == "Producto A", "Nombre de producto 1 incorrecto"

        producto2 = inventario2.buscar_por_id(2)
        assert producto2 is not None, "Producto 2 no encontrado"
        assert producto2.get_nombre() == "Producto B", "Nombre de producto 2 incorrecto"

        print("Test 14 PASADO: Persistencia en archivo funciona correctamente")
    finally:
        # Limpiar archivo temporal
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)


def test_archivo_no_existente():
    """Prueba que el sistema maneja correctamente un archivo que no existe."""
    print("\nTest 15: Manejo de Archivo No Existente")

    archivo_no_existe = "/tmp/inventario_no_existe_test_12345.txt"

    # Asegurar que el archivo no existe
    if os.path.exists(archivo_no_existe):
        os.remove(archivo_no_existe)

    try:
        # Crear inventario con archivo que no existe
        inventario = Inventario(archivo_no_existe)

        # El inventario debería estar vacío pero funcional
        assert inventario.obtener_total_productos() == 0, "Inventario debería estar vacío"

        # Agregar un producto debería crear el archivo
        exito, _ = inventario.agregar_producto(Producto(1, "Producto Test", 5, 50.00))
        assert exito, "No se pudo agregar producto"

        # Verificar que el archivo fue creado
        assert os.path.exists(archivo_no_existe), "El archivo no fue creado"

        print("Test 15 PASADO: Manejo de archivo no existente correcto")
    finally:
        if os.path.exists(archivo_no_existe):
            os.remove(archivo_no_existe)


def test_archivo_corrupto():
    """Prueba que el sistema maneja correctamente un archivo con datos corruptos."""
    print("\nTest 16: Manejo de Archivo Corrupto")

    # Crear archivo temporal con contenido corrupto
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name
        # Escribir líneas válidas e inválidas
        f.write("# Comentario\n")
        f.write("1|Producto Válido|10|100.00\n")
        f.write("línea corrupta sin formato\n")
        f.write("abc|Producto ID inválido|10|100.00\n")
        f.write("2|Otro Producto Válido|5|50.00\n")
        f.write("3|Precio inválido|5|no_es_numero\n")

    try:
        # Cargar inventario con archivo corrupto
        inventario = Inventario(archivo_temp)

        # Solo deben haberse cargado los productos válidos (2)
        total = inventario.obtener_total_productos()
        assert total == 2, f"Esperaba 2 productos válidos, obtuvo {total}"

        # Verificar que los productos válidos se cargaron
        assert inventario.buscar_por_id(1) is not None, "Producto 1 no encontrado"
        assert inventario.buscar_por_id(2) is not None, "Producto 2 no encontrado"

        print("Test 16 PASADO: Manejo de archivo corrupto correcto")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)


def test_ids_duplicados_en_archivo():
    """Prueba que el sistema maneja correctamente IDs duplicados en archivo."""
    print("\nTest 17: Manejo de IDs Duplicados en Archivo")

    # Crear archivo temporal con IDs duplicados
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name
        f.write("1|Producto A|10|100.00\n")
        f.write("1|Producto Duplicado|20|200.00\n")  # ID duplicado
        f.write("2|Producto B|15|150.00\n")

    try:
        # Cargar inventario
        inventario = Inventario(archivo_temp)

        # Solo debe haber 2 productos (ID 1 y 2)
        total = inventario.obtener_total_productos()
        assert total == 2, f"Esperaba 2 productos, obtuvo {total}"

        # El primer producto con ID 1 debe ser "Producto A"
        producto = inventario.buscar_por_id(1)
        assert producto.get_nombre() == "Producto A", "Se cargó el producto duplicado en lugar del original"

        print("Test 17 PASADO: Manejo de IDs duplicados correcto")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)


def test_recargar_inventario():
    """Prueba la funcionalidad de recargar inventario desde archivo."""
    print("\nTest 18: Recargar Inventario desde Archivo")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        archivo_temp = f.name

    try:
        # Crear inventario y agregar productos
        inventario = Inventario(archivo_temp)
        inventario.agregar_producto(Producto(1, "Producto Original", 10, 100.00))

        # Modificar el archivo directamente
        with open(archivo_temp, 'w') as f:
            f.write("2|Producto Modificado|20|200.00\n")

        # Recargar el inventario
        exito, mensaje = inventario.cargar_inventario()

        assert exito, "Error al recargar inventario"
        assert inventario.obtener_total_productos() == 1, "Cantidad de productos incorrecta"
        assert inventario.buscar_por_id(1) is None, "El producto original no debería existir"
        assert inventario.buscar_por_id(2) is not None, "El producto modificado no se encontró"

        print("Test 18 PASADO: Recarga de inventario correcta")
    finally:
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)


def test_ruta_archivo():
    """Prueba que se puede obtener la ruta del archivo de inventario."""
    print("\nTest 19: Obtener Ruta de Archivo")

    ruta_personalizada = "/tmp/mi_inventario_test.txt"

    try:
        inventario = Inventario(ruta_personalizada)
        assert inventario.get_ruta_archivo() == ruta_personalizada, "Ruta de archivo incorrecta"

        # Probar con ruta por defecto
        inventario_default = Inventario()
        assert inventario_default.get_ruta_archivo() == "inventario.txt", "Ruta por defecto incorrecta"

        print("Test 19 PASADO: Obtención de ruta de archivo correcta")
    finally:
        if os.path.exists(ruta_personalizada):
            os.remove(ruta_personalizada)
        if os.path.exists("inventario.txt"):
            os.remove("inventario.txt")

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas del sistema."""
    print("\n" + "="*70)
    print(" EJECUTANDO PRUEBAS DEL SISTEMA DE GESTIÓN DE INVENTARIOS ".center(70))
    print("="*70)
    
    try:
        # Pruebas básicas de productos
        test_crear_producto()
        test_getters_setters()
        test_agregar_producto()
        test_eliminar_producto()
        test_actualizar_cantidad()
        test_actualizar_precio()
        test_buscar_por_nombre()
        test_buscar_por_id()
        test_mostrar_todos()
        test_valor_total_inventario()
        test_str_representation()
        
        # Pruebas de persistencia en archivos
        print("\n" + "-"*70)
        print(" PRUEBAS DE PERSISTENCIA EN ARCHIVOS ".center(70))
        print("-"*70)
        test_producto_to_line()
        test_producto_from_line()
        test_persistencia_archivo()
        test_archivo_no_existente()
        test_archivo_corrupto()
        test_ids_duplicados_en_archivo()
        test_recargar_inventario()
        test_ruta_archivo()

        print("\n" + "="*70)
        print(" ✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE ".center(70))
        print("="*70 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ ERROR: {e}")
        print("\n" + "="*70)
        print(" ❌ ALGUNAS PRUEBAS FALLARON ".center(70))
        print("="*70 + "\n")
        return False
    
    return True

if __name__ == "__main__":
    ejecutar_todas_las_pruebas()
