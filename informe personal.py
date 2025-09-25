# informacion_personal.py

informacion_personal = {
    "nombre": "Justyn Mateo Haz Vera",
    "edad": 19,
    "ciudad": "Esmeraldas",
    "sexo": "Masculino",
    "profesion": "Estudiante"
}
print("Diccionario inicial:")
print(informacion_personal)
print()

# Acceder y modificar 'ciudad'
print("Ciudad actual:", informacion_personal["ciudad"])
informacion_personal["ciudad"] = "Guayaquil"
print("Ciudad modificada a:", informacion_personal["ciudad"])
print()

# Agregar/actualizar 'profesion'
informacion_personal["profesion"] = "Ingeniera de Software"
print("Profesión establecida/actualizada a:", informacion_personal["profesion"])
print()

# Verificar y agregar 'telefono' si no existe
if "telefono" not in informacion_personal:
    informacion_personal["telefono"] = "+593987654321"
    print("Clave 'telefono' no existía. Se ha agregado.")
else:
    print("Clave 'telefono' ya existe con valor:", informacion_personal["telefono"])
print()

# Eliminar 'edad'
edad_eliminada = informacion_personal.pop("edad", None)
print("Edad eliminada (valor anterior):", edad_eliminada)
print()

# Imprimir diccionario final
print("Diccionario final resultado:")
print(informacion_personal)
