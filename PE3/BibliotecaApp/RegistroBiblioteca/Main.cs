using RegistroBiblioteca;

GestorBiblioteca biblioteca = new GestorBiblioteca();
bool salir = false;

while (!salir)
{
    Console.WriteLine("\n= SISTEMA DE BIBLIOTECA =");
    Console.WriteLine("1. Registrar nuevo libro");
    Console.WriteLine("2. Mostrar todos los libros");
    Console.WriteLine("3. Buscar libro por ISBN");
    Console.WriteLine("4. Prestar un libro");
    Console.WriteLine("5. Devolver un libro");
    Console.WriteLine("6. Salir");
    Console.Write("Seleccione una opción: ");

    string? opcion = Console.ReadLine();

    switch (opcion)
    {
        case "1":
            Libro nuevoLibro = new Libro();
            Console.Write("Ingrese ISBN: ");
            nuevoLibro.ISBN = Console.ReadLine() ?? "";
            Console.Write("Ingrese Título: ");
            nuevoLibro.Titulo = Console.ReadLine() ?? "";
            Console.Write("Ingrese Autor: ");
            nuevoLibro.Autor = Console.ReadLine() ?? "";
            Console.Write("Ingrese Año de Publicación: ");
            int.TryParse(Console.ReadLine(), out int anio);
            nuevoLibro.AnioPublicacion = anio;

            biblioteca.RegistrarLibro(nuevoLibro);
            break;

        case "2":
            biblioteca.ListarLibros();
            break;

        case "3":
            Console.Write("Ingrese el ISBN a buscar: ");
            string isbnBuscar = Console.ReadLine() ?? "";
            Libro? buscado = biblioteca.BuscarPorISBN(isbnBuscar);
            if (buscado != null)
                Console.WriteLine($"\nEncontrado: {buscado}");
            else
                Console.WriteLine("\nNo se encontró ningún libro con ese ISBN.");
            break;

        case "4":
            Console.Write("Ingrese el ISBN del libro que desea PRESTAR: ");
            string isbnPrestar = Console.ReadLine() ?? "";
            biblioteca.PrestarLibro(isbnPrestar);
            break;

        case "5":
            Console.Write("Ingrese el ISBN del libro que desea DEVOLVER: ");
            string isbnDevolver = Console.ReadLine() ?? "";
            biblioteca.DevolverLibro(isbnDevolver);
            break;

        case "6":
            salir = true;
            Console.WriteLine("Guardando datos y saliendo del sistema...");
            break;

        default:
            Console.WriteLine("Opción no válida. Intente de nuevo.");
            break;
    }
}