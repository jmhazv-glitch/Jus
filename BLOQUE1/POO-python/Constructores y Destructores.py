class ArchivoLogger:
    """
    Clase que demuestra el uso de constructores y destructores en Python.
    Se encarga de escribir mensajes en un archivo de texto.
    """

    def __init__(self, nombre_archivo):
        """
        CONSTRUCTOR
        Se ejecuta automáticamente cuando se crea un objeto de la clase.
        Inicializa los atributos y abre el archivo.
        """
        self.nombre_archivo = nombre_archivo
        self.archivo = open(self.nombre_archivo, "a")
        print("Constructor ejecutado: archivo abierto correctamente.")

    def escribir_mensaje(self, mensaje):
        """
        Método que escribe un mensaje en el archivo.
        """
        self.archivo.write(mensaje + "\n")
        print("Mensaje escrito en el archivo.")

    def __del__(self):
        """
        DESTRUCTOR
        Se ejecuta automáticamente cuando el objeto es eliminado
        o cuando el programa finaliza.
        Se encarga de cerrar el archivo.
        """
        if self.archivo:
            self.archivo.close()
            print("Destructor ejecutado: archivo cerrado correctamente.")


# ------------------ PROGRAMA PRINCIPAL ------------------

# Creación del objeto (se ejecuta el constructor)
logger = ArchivoLogger("registro.txt")

# Uso del objeto
logger.escribir_mensaje("Hola, este es un mensaje de prueba.")
logger.escribir_mensaje("Demostración de constructores y destructores en Python.")

# Eliminación del objeto (se ejecuta el destructor)
del logger

print("Fin del programa.")
