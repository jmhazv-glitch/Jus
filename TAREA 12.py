# Iteración de arreglos multidimensionales con bucles anidados
# Matriz 3D: [ciudad][semana][día]

# Datos de ejemplo: 2 ciudades, 2 semanas, 7 días
# Estructura: temperaturas[ciudad][semana][día]

temperaturas = [
    [   # Ciudad 0: Quito
        [15, 16, 14, 15, 17, 18, 16],  # Semana 0
        [14, 15, 16, 15, 17, 18, 19]   # Semana 1
    ],
    [   # Ciudad 1: Guayaquil
        [28, 29, 30, 31, 29, 28, 30],  # Semana 0
        [27, 28, 29, 30, 30, 29, 28]   # Semana 1
    ]
]

ciudades = ["Quito", "Guayaquil"]
semanas = ["Semana 1", "Semana 2"]
dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

# Calcular el promedio por ciudad y semana
for i in range(len(ciudades)):  # Iterar ciudades
    print(f"\nCiudad: {ciudades[i]}")
    for j in range(len(semanas)):  # Iterar semanas
        suma = 0
        for k in range(len(dias)):  # Iterar días
            suma += temperaturas[i][j][k]
        promedio = suma / len(dias)
        print(f"  {semanas[j]} → Promedio: {promedio:.2f} °C")
