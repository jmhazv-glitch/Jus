using System;
public class Nodo
{
    public int Valor { get; set; }
    public Nodo? Siguiente { get; set; }

    public Nodo(int valor)
    {
        Valor = valor;
    }
}

public class ListaEnlazada
{
    private Nodo? cabeza;

    public bool EstaVacia()
    {
        return cabeza == null;
    }

    public void InsertarAlFinal(int valor)
    {
        Nodo nuevoNodo = new Nodo(valor);

        if (cabeza == null)
        {
            cabeza = nuevoNodo;
            return;
        }

        Nodo actual = cabeza;
        while (actual.Siguiente != null)
        {
            actual = actual.Siguiente;
        }

        actual.Siguiente = nuevoNodo;
    }

    public void InsertarAlInicio(int valor)
    {
        Nodo nuevoNodo = new Nodo(valor)
        {
            Siguiente = cabeza
        };

        cabeza = nuevoNodo;
    }

    public void EliminarPrimero()
    {
        if (cabeza == null)
        {
            Console.WriteLine("La lista está vacía. No se puede eliminar el primer elemento.");
            return;
        }

        cabeza = cabeza.Siguiente;
        Console.WriteLine("Primer nodo eliminado correctamente.");
    }

    public void Mostrar()
    {
        if (cabeza == null)
        {
            Console.WriteLine("La lista está vacía.");
            return;
        }

        Nodo? actual = cabeza;
        Console.Write("Lista: ");

        while (actual != null)
        {
            Console.Write(actual.Valor);

            if (actual.Siguiente != null)
            {
                Console.Write(" -> ");
            }

            actual = actual.Siguiente;
        }

        Console.WriteLine();
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        ListaEnlazada lista = new ListaEnlazada();
        string opcion = string.Empty;

        do
        {
            Console.Clear();
            Console.WriteLine("SISTEMA DE LISTAS ENLAZADAS");
            Console.WriteLine("1. Insertar al inicio");
            Console.WriteLine("2. Insertar al final");
            Console.WriteLine("3. Eliminar primero");
            Console.WriteLine("4. Mostrar lista");
            Console.WriteLine("5. Salir");
            Console.Write("Seleccione una opción: ");

            opcion = Console.ReadLine() ?? string.Empty;

            switch (opcion)
            {
                case "1":
                    Console.Write("Ingrese un valor entero: ");
                    if (int.TryParse(Console.ReadLine(), out int valorInicio))
                    {
                        lista.InsertarAlInicio(valorInicio);
                        Console.WriteLine("Valor insertado al inicio.");
                    }
                    else
                    {
                        Console.WriteLine("Entrada inválida.");
                    }
                    Pausar();
                    break;

                case "2":
                    Console.Write("Ingrese un valor entero: ");
                    if (int.TryParse(Console.ReadLine(), out int valorFinal))
                    {
                        lista.InsertarAlFinal(valorFinal);
                        Console.WriteLine("Valor insertado al final.");
                    }
                    else
                    {
                        Console.WriteLine("Entrada inválida.");
                    }
                    Pausar();
                    break;

                case "3":
                    lista.EliminarPrimero();
                    Pausar();
                    break;

                case "4":
                    lista.Mostrar();
                    Pausar();
                    break;

                case "5":
                    Console.WriteLine("Saliendo...");
                    break;

                default:
                    Console.WriteLine("Opción no válida.");
                    Pausar();
                    break;
            }
        }
        while (opcion != "5");
    }

    private static void Pausar()
    {
        Console.WriteLine("Presione ENTER para continuar...");
        Console.ReadLine();
    }
}

