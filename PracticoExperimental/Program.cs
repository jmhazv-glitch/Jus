using System;

namespace PracticaEstructuras
{
    public struct Empleado
    {
        public int IdEmpleado;
        public string Nombre;
        public string Departamento;

        public Empleado(int id, string nombre, string departamento)
        {
            IdEmpleado = id;
            Nombre = nombre;
            Departamento = departamento;
        }
    }

    public class GestorAportes
    {
        private Empleado[] empleados;
        
        private double[,] matrizAportes; 
        
        private int capacidadMaxima;
        public int empleadosRegistrados { get; private set; }

        public GestorAportes(int capacidad)
        {
            this.capacidadMaxima = capacidad;
            this.empleadosRegistrados = 0;
            this.empleados = new Empleado[capacidad];
            this.matrizAportes = new double[capacidad, 12];
        }

        public bool RegistrarEmpleado(int id, string nombre, string departamento)
        {
            for (int i = 0; i < empleadosRegistrados; i++)
            {
                if (empleados[i].IdEmpleado == id) return false;
            }

            if (empleadosRegistrados < capacidadMaxima)
            {
                empleados[empleadosRegistrados] = new Empleado(id, nombre, departamento);
                empleadosRegistrados++;
                return true; 
            }
            return false; 
        }

        public bool RegistrarAporte(int idEmpleado, int mes, double monto)
        {
            if (mes < 1 || mes > 12) return false;

            for (int i = 0; i < empleadosRegistrados; i++)
            {
                if (empleados[i].IdEmpleado == idEmpleado)
                {
                    matrizAportes[i, mes - 1] += monto; 
                    return true;
                }
            }
            return false; 
        }

        
        public void VerReporteGeneral()
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.DarkMagenta;
            Console.WriteLine("                       REPORTE GENERAL DE APORTES                              ");
            Console.WriteLine("===============================================================================");
            Console.ResetColor();

            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine($"{"ID",-5} | {"Nombre",-15} | {"Ene",-8} | {"Feb",-8} | {"Mar",-8} | {"TOTAL",-10}");
            Console.WriteLine("-------------------------------------------------------------------------------");
            Console.ResetColor();

            if (empleadosRegistrados == 0)
            {
                Console.ForegroundColor = ConsoleColor.White;
                Console.WriteLine("                    No hay empleados registrados aún.                          ");
                Console.ResetColor();
                return;
            }

            for (int i = 0; i < empleadosRegistrados; i++)
            {
                double total = 0;
                string fila = $"{empleados[i].IdEmpleado,-5} | {empleados[i].Nombre,-15}";
                
                for (int m = 0; m < 12; m++)
                {
                    double aporteMes = matrizAportes[i, m];
                    total += aporteMes;

                    if(m < 3) 
                    {
                        fila += $" | {aporteMes,8:C2}"; 
                    }
                }
                fila += $" | {total,10:C2}";
                Console.WriteLine(fila);
            }
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine("===============================================================================\n");
            Console.ResetColor();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            GestorAportes gestor = new GestorAportes(50);
            string opcion = "";

            do
            {
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.DarkMagenta;
                Console.WriteLine("     SISTEMA DE APORTES - ASOCIACIÓN DE EMPLEADOS   ");
                Console.ResetColor();
                Console.WriteLine("1. Registrar Empleado");
                Console.WriteLine("2. Registrar Aporte mensual");
                Console.WriteLine("3. Ver Reporte General de Aportes");
                Console.WriteLine("4. Salir");
                Console.WriteLine("----------------------------------------------------");
                Console.Write("Seleccione una opción: ");
                
                opcion = Console.ReadLine();

                switch (opcion)
                {
                    case "1":
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Blue;
                        Console.WriteLine("-- REGISTRAR NUEVO EMPLEADO --");
                        Console.ResetColor();
                        
                        try
                        {
                            Console.Write("ID del Empleado (número): ");
                            int id = int.Parse(Console.ReadLine());
                            
                            Console.Write("Nombre: ");
                            string nombre = Console.ReadLine();
                            
                            Console.Write("Departamento: ");
                            string depto = Console.ReadLine();

                            if (gestor.RegistrarEmpleado(id, nombre, depto))
                            {
                                Console.ForegroundColor = ConsoleColor.Green;
                                Console.WriteLine("\n¡Empleado registrado con éxito!");
                            }
                            else
                            {
                                Console.ForegroundColor = ConsoleColor.Red;
                                Console.WriteLine("\nError: El ID ya existe o la base de datos está llena.");
                            }
                        }
                        catch
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\nError: Entrada inválida. Por favor, intente de nuevo.");
                        }
                        PausarYContinuar();
                        break;

                    case "2":
                        Console.Clear();
                        Console.ForegroundColor = ConsoleColor.Blue;
                        Console.WriteLine("-- REGISTRAR APORTE MENSUAL --");
                        Console.ResetColor();
                        
                        try
                        {
                            Console.Write("ID del Empleado: ");
                            int idAporte = int.Parse(Console.ReadLine());
                            
                            Console.Write("Mes del aporte (1=Ene, 2=Feb... 12=Dic): ");
                            int mes = int.Parse(Console.ReadLine());
                            
                            Console.Write("Monto a registrar ($): ");
                            double monto = double.Parse(Console.ReadLine());

                            if (gestor.RegistrarAporte(idAporte, mes, monto))
                            {
                                Console.ForegroundColor = ConsoleColor.Green;
                                Console.WriteLine("\n¡Aporte registrado correctamente!");
                            }
                            else
                            {
                                Console.ForegroundColor = ConsoleColor.Red;
                                Console.WriteLine("\nError al registrar (ID no encontrado o mes inválido).");
                            }
                        }
                        catch
                        {
                            Console.ForegroundColor = ConsoleColor.Red;
                            Console.WriteLine("\nError: Entrada inválida. Asegúrese de ingresar números válidos.");
                        }
                        PausarYContinuar();
                        break;

                    case "3":
                        gestor.VerReporteGeneral();
                        PausarYContinuar();
                        break;

                    case "4":
                        Console.ForegroundColor = ConsoleColor.Magenta;
                        Console.WriteLine("\nSaliendo del sistema. ¡Hasta luego!");
                        Console.ResetColor();
                        break;

                    default:
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\nOpción no válida. Intente de nuevo.");
                        PausarYContinuar();
                        break;
                }
            } while (opcion != "4");
        }
        
        static void PausarYContinuar()
        {
            Console.ResetColor();
            Console.WriteLine("\nPresione ENTER para continuar...");
            Console.ReadLine();
        }
    }
}