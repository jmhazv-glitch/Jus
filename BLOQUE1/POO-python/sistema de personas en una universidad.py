# Programa que demuestra los conceptos de POO en Python(sistema de personas en una universidad)
# Autor: Justyn
# Tema: Clases, Objetos, Herencia, Encapsulación y Polimorfismo

# Clase base
class Persona:
    def __init__(self, nombre, edad):
        # Atributos encapsulados (privados)
        self.__nombre = nombre
        self.__edad = edad

    # Métodos getters (encapsulación)
    def get_nombre(self):
        return self.__nombre

    def get_edad(self):
        return self.__edad

    # Metodo que será sobrescrito (polimorfismo)
    def descripcion(self):
        return f"Persona llamada {self.__nombre}, edad {self.__edad}"


# Clase derivada (herencia)
class Estudiante(Persona):
    def __init__(self, nombre, edad, carrera):
        # Llamada al constructor de la clase base
        super().__init__(nombre, edad)
        self.carrera = carrera

    # Metodo sobrescrito (polimorfismo)
    def descripcion(self):
        return f"Estudiante de {self.carrera}, nombre {self.get_nombre()}, edad {self.get_edad()}"


# Programa principal
if __name__ == "__main__":
    # Creación de objetos
    persona1 = Persona("Carlos", 40)
    estudiante1 = Estudiante("Ana", 20, "Ingeniería en Sistemas")

    # Uso de métodos
    print(persona1.descripcion())
    print(estudiante1.descripcion())
