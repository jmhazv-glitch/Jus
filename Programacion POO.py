# --------------------------------------------------------
# Programa: Promedio Semanal del Clima (Programación Tradicional)
# Descripción:
#   Solicita las temperaturas diarias mediante funciones
#   y calcula el promedio semanal.
# --------------------------------------------------------

# Función para ingresar las temperaturas de los 7 días
def ingresar_temperaturas():
    temperaturas = []
    print("Ingreso de temperaturas semanales:")
    for i in range(7):
        temp = float(input(f"Ingrese la temperatura del día {i + 1}: "))
        temperaturas.append(temp)
    return temperaturas

# Función para calcular el promedio
def calcular_promedio(temps):
    return sum(temps) / len(temps)

# Función principal
def main():
    temps = ingresar_temperaturas()
    promedio = calcular_promedio(temps)
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

# Ejecución del programa
if __name__ == "__main__":
    main()
