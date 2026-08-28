namespace RegistroBiblioteca;
// seccion de libro 
public class Libro
{
    public string ISBN { get; set; } = string.Empty;
    public string Titulo { get; set; } = string.Empty;
    public string Autor { get; set; } = string.Empty;
    public int AnioPublicacion { get; set; }
    public bool Disponible { get; set; } = true;

    public override string ToString()
    {
        string estado = Disponible ? "Disponible" : "Prestado";
        return $"[{ISBN}] '{Titulo}' - {Autor} ({AnioPublicacion}) | Estado: {estado}";
    }
}