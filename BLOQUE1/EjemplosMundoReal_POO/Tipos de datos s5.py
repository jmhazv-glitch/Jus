"""
Programa: Conversor de temperatura
Descripción: Este programa convierte temperaturas de grados Celsius a Fahrenheit.
Autor: Justyn
"""
def convertir_celsius_a_fahrenheit(temperatura_celsius):
    """
    Convierte grados Celsius a Fahrenheit
    """
    temperatura_fahrenheit = (temperatura_celsius * 9 / 5) + 32
    return temperatura_fahrenheit

# Solicitar datos al usuario
nombre_usuario = input("Ingrese su nombre: ")
ejecutar_programa = True

print(f"\nHola {nombre_usuario}, bienvenido al conversor de temperatura 🌡️")

while ejecutar_programa:
    temperatura_celsius = float(input("\nIngrese la temperatura en grados Celsius: "))

    resultado = convertir_celsius_a_fahrenheit(temperatura_celsius)

    print(f"La temperatura en Fahrenheit es: {resultado:.2f} °F")

    opcion = int(input("\n¿Desea convertir otra temperatura? (1 = Sí, 0 = No): "))

    if opcion == 0:
        ejecutar_programa = False
        print("\nGracias por usar el programa. ¡Hasta luego!")
