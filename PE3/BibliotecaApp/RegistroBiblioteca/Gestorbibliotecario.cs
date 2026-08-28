using System.Text.Json;
using System.IO;

namespace RegistroBiblioteca;

public class GestorBiblioteca
{
    private Dictionary<string, Libro> _catalogo = new Dictionary<string, Libro>(StringComparer.OrdinalIgnoreCase);
    
    private HashSet<string> _autoresUnicos = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
    
    private const string ArchivoDatos = "libros_guardados.json";

    public GestorBiblioteca()
    {
        CargarDatos();
    }

    public void RegistrarLibro(Libro libro)
    {
        if (_catalogo.ContainsKey(libro.ISBN))
        {
            Console.WriteLine($"\nError: Ya existe un libro con el ISBN {libro.ISBN}.");
            return;
        }

        _catalogo.Add(libro.ISBN, libro);
        
        _autoresUnicos.Add(libro.Autor);
        
        GuardarDatos(); 
        Console.WriteLine("\n¡Libro registrado y guardado con éxito!");
    }

    public Libro? BuscarPorISBN(string isbn)
    {
        return _catalogo.GetValueOrDefault(isbn);
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
        Console.WriteLine($"\n¡Éxito! El libro '{libro.Titulo}' ha sido devuelto y está disponible.");
    }

    public void ListarLibros()
    {
        if (_catalogo.Count == 0)
        {
            Console.WriteLine("\nNo hay libros registrados en la biblioteca.");
            return;
        }

        Console.WriteLine("\n--- CATÁLOGO DE LA BIBLIOTECA ---");
        // CORRECCIÓN: Para imprimir desde un diccionario, recorremos sus Valores (.Values)
        foreach (var libro in _catalogo.Values)
        {
            Console.WriteLine(libro);
        }

        Console.WriteLine("\n--- AUTORES REGISTRADOS (CONJUNTO) ---");
        foreach (var autor in _autoresUnicos)
        {
            Console.WriteLine($"- {autor}");
        }
    }

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
            
            var datosRecuperados = JsonSerializer.Deserialize<Dictionary<string, Libro>>(json);
            
            if (datosRecuperados != null)
            {
                _catalogo = datosRecuperados;
                
                foreach (var libro in _catalogo.Values)
                {
                    _autoresUnicos.Add(libro.Autor);
                }
            }
        }
    }
}