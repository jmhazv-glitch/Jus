# Ejemplo del Mundo Real usando Programación Orientada a Objetos
# Caso: Sistema básico de una tienda

class Producto:
    """
    Clase que representa un producto de la tienda
    """
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def mostrar_info(self):
        return f"Producto: {self.nombre}, Precio: ${self.precio}"


class Carrito:
    """
    Clase que representa el carrito de compras
    """
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)
        print(f"{producto.nombre} agregado al carrito.")

    def calcular_total(self):
        total = 0
        for producto in self.productos:
            total += producto.precio
        return total


# Programa principal
if __name__ == "__main__":
    # Crear productos
    producto1 = Producto("Laptop", 800)
    producto2 = Producto("Mouse", 20)

    # Crear carrito
    carrito = Carrito()

    # Agregar productos al carrito
    carrito.agregar_producto(producto1)
    carrito.agregar_producto(producto2)

    # Mostrar total a pagar
    print(f"Total a pagar: ${carrito.calcular_total()}")
