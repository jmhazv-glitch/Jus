using System;
using System.Collections.Generic;
using System.Diagnostics;

class Vuelo
{
    public string Destino { get; set; }
    public int Precio { get; set; }

    public Vuelo(string destino, int precio)
    {
        Destino = destino;
        Precio = precio;
    }
}

class GrafoVuelos
{
    private Dictionary<string, List<Vuelo>> rutas;

    public GrafoVuelos()
    {
        rutas = new Dictionary<string, List<Vuelo>>();
    }

    public void AgregarCiudad(string ciudad)
    {
        if (!rutas.ContainsKey(ciudad))
        {
            rutas[ciudad] = new List<Vuelo>();
        }
    }

    public void AgregarVuelo(string origen, string destino, int precio)
    {
        if (!rutas.ContainsKey(origen)) AgregarCiudad(origen);
        if (!rutas.ContainsKey(destino)) AgregarCiudad(destino);

        rutas[origen].Add(new Vuelo(destino, precio));
    }

    // Muestra todas las conexiones
    public void MostrarRutas()
    {
        Console.WriteLine("--- Base de Datos de Vuelos ---");
        foreach (var ruta in rutas)
        {
            string origen = ruta.Key;
            List<string> conexiones = new List<string>();
            
            foreach (var vuelo in ruta.Value)
            {
                conexiones.Add($"{vuelo.Destino} (${vuelo.Precio})");
            }

            string conexionesStr = conexiones.Count > 0 ? string.Join(", ", conexiones) : "Sin vuelos de salida";
            Console.WriteLine($"{origen} -> {conexionesStr}");
        }
    }

    // Algoritmo de Dijkstra 
    public (List<string> ruta, int costo, double tiempo) EncontrarVueloMasBarato(string origen, string destino)
    {
        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        Dictionary<string, int> distancias = new Dictionary<string, int>();
        Dictionary<string, string> previos = new Dictionary<string, string>();
        HashSet<string> noVisitados = new HashSet<string>(rutas.Keys);

        foreach (var ciudad in rutas.Keys)
        {
            distancias[ciudad] = int.MaxValue;
            previos[ciudad] = null;
        }
        distancias[origen] = 0;

        while (noVisitados.Count > 0)
        {
            string ciudadActual = null;
            foreach (var ciudad in noVisitados)
            {
                if (ciudadActual == null || distancias[ciudad] < distancias[ciudadActual])
                {
                    ciudadActual = ciudad;
                }
            }

            // Si la distancia es infinito o ya llegamos al destino, terminamos
            if (distancias[ciudadActual] == int.MaxValue) break;
            if (ciudadActual == destino) break;

            noVisitados.Remove(ciudadActual);

            // Analizar los vuelos desde la ciudad actual
            foreach (var vuelo in rutas[ciudadActual])
            {
                int costoAlternativo = distancias[ciudadActual] + vuelo.Precio;
                if (costoAlternativo < distancias[vuelo.Destino])
                {
                    distancias[vuelo.Destino] = costoAlternativo;
                    previos[vuelo.Destino] = ciudadActual;
                }
            }
        }

        stopwatch.Stop();
        double tiempoEjecucion = stopwatch.Elapsed.TotalMilliseconds;

        List<string> rutaOptima = new List<string>();
        string actual = destino;
        while (actual != null)
        {
            rutaOptima.Insert(0, actual); 
            actual = previos[actual];
        }

        // Por si no encuantra una ruta por las dudas
        if (distancias[destino] == int.MaxValue)
        {
            return (new List<string>(), int.MaxValue, tiempoEjecucion);
        }

        return (rutaOptima, distancias[destino], tiempoEjecucion);
    }
}

// Clase de ejecucion
class Prin
{
    static void Main()
    {
        GrafoVuelos sistemaVuelos = new GrafoVuelos();

        //  Cargamos las ciudades (Nodos)
        sistemaVuelos.AgregarCiudad("Quito");
        sistemaVuelos.AgregarCiudad("Guayaquil");
        sistemaVuelos.AgregarCiudad("Cuenca");
        sistemaVuelos.AgregarCiudad("Manta");

        //  Cargamos los vuelos (Aristas: origen, destino, precio)
        sistemaVuelos.AgregarVuelo("Quito", "Guayaquil", 55);
        sistemaVuelos.AgregarVuelo("Quito", "Manta", 45);
        sistemaVuelos.AgregarVuelo("Guayaquil", "Cuenca", 30);
        sistemaVuelos.AgregarVuelo("Manta", "Guayaquil", 20);
        sistemaVuelos.AgregarVuelo("Manta", "Cuenca", 60);

        //  Ejecutamos la reporteria
        sistemaVuelos.MostrarRutas();

        //  Buscamos el vuelo mas barato
        Console.WriteLine("\n--- Busqueda de Vuelo Optimo ---");
        var resultado = sistemaVuelos.EncontrarVueloMasBarato("Quito", "Cuenca");
        
        Console.WriteLine($"Ruta mas barata: {string.Join(" -> ", resultado.ruta)}");
        Console.WriteLine($"Costo total: ${resultado.costo}");
        Console.WriteLine($"Tiempo de ejecución del algoritmo: {resultado.tiempo:F4} ms");
    }
}