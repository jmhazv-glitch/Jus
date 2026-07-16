using System;
using System.Collections.Generic;

namespace EstructuraDatosPractica2
{
    // Clase que representa el objeto a almacenar en la estructura
    public class Persona
    {
        public string Nombre { get; set; }
        public int TicketID { get; set; }

        public Persona(string nombre, int ticketID)
        {
            Nombre = nombre;
            TicketID = ticketID;
        }

        public override string ToString()
        {
            return $"Ticket #{TicketID} - {Nombre}";
        }
    }

    // Clase que maneja la estructura de datos (Cola)
    public class AtraccionParque
    {
        private Queue<Persona> filaEspera;
        private int capacidadMaxima;

        public AtraccionParque(int capacidad)
        {
            // Instanciación de la Cola
            filaEspera = new Queue<Persona>();
            capacidadMaxima = capacidad;
        }

        // Método para agregar elementos (Enqueue)
        public void RegistrarPersona(Persona persona)
        {
            if (filaEspera.Count < capacidadMaxima)
            {
                filaEspera.Enqueue(persona);
                Console.WriteLine($"Registrado en fila: {persona.Nombre}");
            }
            else
            {
                Console.WriteLine($"\n[ALERTA] Atracción llena. {persona.Nombre} no puede ingresar a esta ronda.");
            }
        }

        // Reportería: Visualizar y consultar elementos de la Cola
        public void MostrarFila()
        {
            Console.WriteLine("\n--- Estado Actual de la Fila (Reportería) ---");
            if (filaEspera.Count == 0)
            {
                Console.WriteLine("La fila se encuentra vacía.");
                return;
            }

            foreach (var persona in filaEspera)
            {
                Console.WriteLine(persona.ToString());
            }
            Console.WriteLine($"Total de personas en fila: {filaEspera.Count}/{capacidadMaxima}\n");
        }

        // Método para procesar la fila (Dequeue)
        public void ProcesarFila()
        {
            Console.WriteLine("\n--- Iniciando ingreso a los 30 asientos ---");
            while (filaEspera.Count > 0)
            {
                Persona p = filaEspera.Dequeue(); // Extrae el elemento respetando FIFO
                Console.WriteLine($"Asignando asiento a: {p.Nombre} (Ticket #{p.TicketID})");
            }
            Console.WriteLine("Todos los asientos han sido asignados exitosamente.");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            AtraccionParque montañaRusa = new AtraccionParque(30);

            Console.WriteLine("--- Abriendo puertas del parque ---");
            for (int i = 1; i <= 30; i++)
            {
                montañaRusa.RegistrarPersona(new Persona($"Visitante {i}", 1000 + i));
            }

            montañaRusa.MostrarFila();

            montañaRusa.RegistrarPersona(new Persona("Visitante Rezago", 1031));

            montañaRusa.ProcesarFila();

            montañaRusa.MostrarFila();
        }
    }
}
