using System.Text.Json;
using System.IO;

namespace RegistroBiblioteca;

public class GestorBiblioteca
{
    private List<Libro> _catalogo = new();
    
    private const string ArchivoDatos = "libros_guardados.json";

    public GestorBiblioteca()
    {
        CargarDatos();
    }

    public void RegistrarLibro(Libro libro)
    {
        if (_catalogo.Exists(l => l.ISBN == libro.ISBN))
        {
            Console.WriteLine($"\nError: Ya existe un libro con el ISBN {libro.ISBN}.");
            return;
        }

        _catalogo.Add(libro);
        GuardarDatos(); 
        Console.WriteLine("\n¡Libro registrado y guardado con éxito!");
    }

    public Libro? BuscarPorISBN(string isbn)
    {
        return _catalogo.FirstOrDefault(l => l.ISBN.Equals(isbn, StringComparison.OrdinalIgnoreCase));
    }

    public void PrestarLibro(string isbn)
    {
        var libro = BuscarPorISBN(isbn);
        if (libro == null)
        {
            Console.WriteLine("\nError: No se encontró ningún libro con ese ISBN.");
            return;
        }

        if (!libro.Disponible)
        {
            Console.WriteLine("\nEl libro ya se encuentra prestado a otra persona.");
            return;
        }

        libro.Disponible = false;
        GuardarDatos(); 
        Console.WriteLine($"\n¡Éxito! Has prestado el libro: '{libro.Titulo}'.");
    }

    public void DevolverLibro(string isbn)
    {
        var libro = BuscarPorISBN(isbn);
        if (libro == null)
        {
            Console.WriteLine("\nError: No se encontró ningún libro con ese ISBN.");
            return;
        }

        if (libro.Disponible)
        {
            Console.WriteLine("\nEl libro ya consta como disponible en la biblioteca.");
            return;
        }

        libro.Disponible = true; 
        GuardarDatos(); 
        Console.WriteLine($"\n¡Exito! El libro '{libro.Titulo}' ha sido devuelto y está disponible.");
    }

    public void ListarLibros()
    {
        if (_catalogo.Count == 0)
        {
            Console.WriteLine("\nNo hay libros registrados en la biblioteca.");
            return;
        }

        Console.WriteLine("\n--- CATÁLOGO DE LA BIBLIOTECA ---");
        foreach (var libro in _catalogo)
        {
            Console.WriteLine(libro);
        }
    }

           //seccion para gurdasr los datos y que no se pierdan 
    private void GuardarDatos()
    {
        var opciones = new JsonSerializerOptions { WriteIndented = true };
        string json = JsonSerializer.Serialize(_catalogo, opciones);
        
        File.WriteAllText(ArchivoDatos, json);
    }

    private void CargarDatos()
    {
        if (File.Exists(ArchivoDatos))
        {
            string json = File.ReadAllText(ArchivoDatos);
            var datosRecuperados = JsonSerializer.Deserialize<List<Libro>>(json);
            
            if (datosRecuperados != null)
            {
                _catalogo = datosRecuperados;
            }
        }
    }
}