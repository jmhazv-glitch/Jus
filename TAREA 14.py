# CalculoDescuentoPython.py

def calcular_descuento(monto_total, porcentaje_descuento=10):
    """
    Calcula el monto de descuento aplicando el porcentaje sobre el monto total.
    :param monto_total: Valor total de la compra
    :param porcentaje_descuento: Porcentaje de descuento (10% por defecto)
    :return: Monto del descuento
    """
    descuento = monto_total * (porcentaje_descuento / 100)
    return descuento


# Programa principal
if __name__ == "__main__":
    # Primera llamada: usando el descuento por defecto (10%)
    monto1 = 200
    descuento1 = calcular_descuento(monto1)
    print(f"Compra: ${monto1}, Descuento aplicado: ${descuento1}, Total a pagar: ${monto1 - descuento1}")

    # Segunda llamada: especificando un porcentaje diferente
    monto2 = 500
    descuento2 = calcular_descuento(monto2, 15)
    print(f"Compra: ${monto2}, Descuento aplicado: ${descuento2}, Total a pagar: ${monto2 - descuento2}")
