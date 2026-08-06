using System;

namespace Ejercicio_2
{
    class MainClass
    {
        public static void Main(string[] args)
        {
            Console.WriteLine ("Escribe tu nombre bro");
            String nombre = Console.ReadLine ();

            Console.WriteLine ("Escribe una cuidad");
            String cuidad = Console.ReadLine ();

            Console.WriteLine ("Hola " + nombre + "bienvenida a "+ cuidad);

            Console.ReadLine();
        
        }
    }
}