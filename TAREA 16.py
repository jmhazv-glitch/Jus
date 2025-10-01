# Abrimos  el archivo "my_notes.txt" en modo escritura ("w").
# Con write() agregamos líneas de texto personal.
with open("my_notes.txt", "w") as file:
    file.write("Primera nota: Estoy aprendiendo a trabajar con archivos en Python.\n")
    file.write("Segunda nota: Es importante cerrar siempre los archivos después de usarlos.\n")
    file.write("Tercera nota: La práctica constante ayuda a mejorar las habilidades de programación.\n")

# Abrimos el archivo en modo lectura ("r").
# Usamos readline() dentro de un bucle para leer línea por línea.
with open("my_notes.txt", "r") as file:
    print("Contenido del archivo my_notes.txt:\n")
    line = file.readline()  # Leemos la primera línea
    while line:  # Mientras no esté vacía
        print(line.strip())  # .strip() elimina saltos de línea extra
        line = file.readline()  # Leemos la siguiente línea

# Nota:
# Usamos "with open()" porque asegura que el archivo se cierre automáticamente
# después de terminar la operación (no hace falta usar file.close()).
