class Personaje:

    def __init__(self, nombre, fuerza, inteligencia, defensa, vida):
        self.nombre = nombre
        self.fuerza = fuerza
        self.inteligencia = inteligencia
        self.defensa = defensa
        self.vida = vida

    def atributos(self):
        print("\n", self.nombre, ":", sep="")
        print("·Fuerza:", self.fuerza)
        print("·Inteligencia:", self.inteligencia)
        print("·Defensa:", self.defensa)
        print("·Vida:", self.vida)

    def esta_vivo(self):
        return self.vida > 0

    def morir(self):
        self.vida = 0
        print(self.nombre, "ha muerto en combate")

    def daño(self, enemigo):
        return self.fuerza - enemigo.defensa

    def atacar(self, enemigo):
        daño = self.daño(enemigo)

        if daño < 0:   # Evita daño negativo
            daño = 0

        enemigo.vida -= daño
        print(self.nombre, "causa", daño, "de daño a", enemigo.nombre)

        if enemigo.esta_vivo():
            print("Vida restante de", enemigo.nombre, ":", enemigo.vida)
        else:
            enemigo.morir()


# CLASE NINJA

class Ninja(Personaje):

    def __init__(self, nombre, fuerza, inteligencia, defensa, vida, sigilo):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.sigilo = sigilo  # Multiplica el daño en ataques sorpresa

    def atributos(self):
        super().atributos()
        print("·Sigilo:", self.sigilo)

    def daño(self, enemigo):
        # Polimorfismo: daño basado en fuerza + sigilo
        return (self.fuerza * self.sigilo) - enemigo.defensa


#  CLASE ASESINO

class Asesino(Personaje):

    def __init__(self, nombre, fuerza, inteligencia, defensa, vida, critico):
        super().__init__(nombre, fuerza, inteligencia, defensa, vida)
        self.critico = critico  # Probabilidad de ataque critico

    def atributos(self):
        super().atributos()
        print("·Golpe crítico:", self.critico)

    def daño(self, enemigo):
        # Polimorfismo: daño basado en inteligencia + probabilidad crítica
        daño_base = self.inteligencia * 2
        daño_total = daño_base + self.critico

        return daño_total - enemigo.defensa


#  FUNCIÓN DE COMBATE

def combate(j1, j2):
    turno = 1
    while j1.esta_vivo() and j2.esta_vivo():
        print("\n======== Turno", turno, "========")

        j1.atacar(j2)
        if j2.esta_vivo():
            j2.atacar(j1)

        turno += 1

    print("\n===== FIN DEL COMBATE =====")
    if j1.esta_vivo():
        print("Ganador:", j1.nombre)
    else:
        print("Ganador:", j2.nombre)


#  CREACIÓN DE PERSONAJES

ninja = Ninja("Shadow", 12, 10, 4, 85, sigilo=3)
asesino = Asesino("Blade", 8, 14, 3, 90, critico=7)

ninja.atributos()
asesino.atributos()

combate(ninja, asesino)

