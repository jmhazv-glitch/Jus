# Funcion para calcular la temperatura promedio

def calcular_promedios(temperatura, ciudades):

    promedios = {}

    for i, ciudad in enumerate(ciudades):
        suma_total = 0
        contador = 0
        for semana in temperatura[i]:
            for dia in semana:
                suma_total+= dia
                contador += 1
        promedios [ciudad] = suma_total / contador
    return promedios


# Datos de ejemplos: 3 cuidades, 4 semnas, 7 dias por semana
temperaturas = [
    [  # Ciudad 0: Quito
        [15, 16, 14, 15, 17, 18, 16],
        [14, 15, 16, 15, 17, 18, 19],
        [16, 17, 15, 16, 18, 17, 16],
        [15, 14, 16, 17, 15, 16, 18]
    ],
    [  # Ciudad 1: Guayaquil
        [28, 29, 30, 31, 29, 28, 30],
        [27, 28, 29, 30, 30, 29, 28],
        [29, 30, 31, 32, 30, 29, 28],
        [30, 29, 31, 32, 30, 31, 29]
    ],
    [  # Ciudad 2: Cuenca
        [18, 17, 16, 18, 19, 17, 16],
        [19, 18, 17, 18, 19, 20, 18],
        [17, 18, 19, 17, 18, 19, 20],
        [18, 19, 18, 17, 18, 19, 17]
    ]
]
ciudades =["Quito","Guayaquil","Cuenca"]

#Llamar a la funcion
promedios = calcular_promedios(temperaturas, ciudades)

#Mostrar resultados
for ciudad, promedio in promedios.items():
    print(f"La temperatura promedio en {ciudad} es {promedio:.2f} °C")





