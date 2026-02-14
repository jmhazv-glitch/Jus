"""
Modulo test_sistema.py
Pruebas automatizadas para el Sistema de Gestión de Inventarios.
"""

from producto import Producto
from inventario import Inventario

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
    inventario = Inventario()
    producto1 = Producto(1, "Monitor", 20, 299.99)
    producto2 = Producto(2, "Webcam", 30, 79.99)
    
    # Agregar productos
    assert inventario.agregar_producto(producto1) == True, "Error al agregar producto1"
    assert inventario.agregar_producto(producto2) == True, "Error al agregar producto2"
    
    # Intentar agregar producto con ID duplicado
    producto_duplicado = Producto(1, "Otro producto", 5, 10.00)
    assert inventario.agregar_producto(producto_duplicado) == False, "No se detectó ID duplicado"
    
    assert inventario.obtener_total_productos() == 2, "Error en cantidad de productos"
    
    print("Test 3 PASADO: Productos agregados correctamente")

def test_eliminar_producto():
    """Prueba eliminar productos del inventario."""
    print("\nTest 4: Eliminar Producto")
    inventario = Inventario()
    producto = Producto(1, "Auriculares", 40, 59.99)
    
    inventario.agregar_producto(producto)
    assert inventario.obtener_total_productos() == 1, "Error al verificar cantidad inicial"
    
    # Eliminar producto existente
    assert inventario.eliminar_producto(1) == True, "Error al eliminar producto existente"
    assert inventario.obtener_total_productos() == 0, "Error al verificar cantidad después de eliminar"
    
    # Intentar eliminar producto inexistente
    assert inventario.eliminar_producto(999) == False, "No se detectó producto inexistente"
    
    print("Test 4 PASADO: Producto eliminado correctamente")

def test_actualizar_cantidad():
    """Prueba actualizar la cantidad de un producto."""
    print("\nTest 5: Actualizar Cantidad")
    inventario = Inventario()
    producto = Producto(1, "Cable USB", 100, 9.99)
    
    inventario.agregar_producto(producto)
    
    # Actualizar cantidad
    assert inventario.actualizar_cantidad(1, 150) == True, "Error al actualizar cantidad"
    assert producto.get_cantidad() == 150, "Cantidad no actualizada correctamente"
    
    # Intentar actualizar producto inexistente
    assert inventario.actualizar_cantidad(999, 100) == False, "No se detectó producto inexistente"
    
    print("Test 5 PASADO: Cantidad actualizada correctamente")

def test_actualizar_precio():
    """Prueba actualizar el precio de un producto."""
    print("\nTest 6: Actualizar Precio")
    inventario = Inventario()
    producto = Producto(1, "SSD 1TB", 25, 149.99)
    
    inventario.agregar_producto(producto)
    
    # Actualizar precio
    assert inventario.actualizar_precio(1, 129.99) == True, "Error al actualizar precio"
    assert producto.get_precio() == 129.99, "Precio no actualizado correctamente"
    
    # Intentar actualizar producto inexistente
    assert inventario.actualizar_precio(999, 100.00) == False, "No se detectó producto inexistente"
    
    print("Test 6 PASADO: Precio actualizado correctamente")

def test_buscar_por_nombre():
    """Prueba la búsqueda de productos por nombre."""
    print("\nTest 7: Buscar por Nombre")
    inventario = Inventario()
    
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

def test_buscar_por_id():
    """Prueba la búsqueda de productos por ID."""
    print("\nTest 8: Buscar por ID")
    inventario = Inventario()
    
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

def test_mostrar_todos():
    """Prueba obtener todos los productos."""
    print("\nTest 9: Mostrar Todos los Productos")
    inventario = Inventario()
    
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

def test_valor_total_inventario():
    """Prueba el cálculo del valor total del inventario."""
    print("\nTest 10: Valor Total del Inventario")
    inventario = Inventario()
    
    # Agregar productos con valores conocidos
    # Producto 1: 10 unidades x $100 = $1000
    # Producto 2: 20 unidades x $50 = $1000
    # Total esperado: $2000
    inventario.agregar_producto(Producto(1, "Producto A", 10, 100.00))
    inventario.agregar_producto(Producto(2, "Producto B", 20, 50.00))
    
    valor_total = inventario.obtener_valor_total_inventario()
    assert valor_total == 2000.00, f"Esperaba $2000, obtuvo ${valor_total}"
    
    print("Test 10 PASADO: Cálculo de valor total correcto")

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

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas del sistema."""
    print("\n" + "="*70)
    print(" EJECUTANDO PRUEBAS DEL SISTEMA DE GESTIÓN DE INVENTARIOS ".center(70))
    print("="*70)
    
    try:
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
        
        print("\n" + "="*70)
        print(" TODAS LAS PRUEBAS PASARON EXITOSAMENTE ".center(70))
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
