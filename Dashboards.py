# Dashboard personalizado por Haz Vera Justyn Mateo
# Fecha:29/1/2026
# Modificaciones realizadas:
# - Adaptado para mis carpetas de proyecto: EjemplosMundoReal_POO y POO-python
# - Personalizado el menu principal con titulos mas descriptivos
# - Agregado soporte para mostrar archivos .py directamente en carpetas
# - Mejorada la experiencia de usuario con emojis y formato

import os
import subprocess

def mostrar_codigo(ruta_script):
    """Muestra el código de un archivo Python"""
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n{'=' * 60}")
            print(f"--- Código de {os.path.basename(ruta_script)} ---")
            print(f"{'=' * 60}\n")
            print(codigo)
            print(f"\n{'=' * 60}")
            return codigo
    except FileNotFoundError:
        print("❌ El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"❌ Ocurrió un error al leer el archivo: {e}")
        return None


def ejecutar_codigo(ruta_script):
    """Ejecuta un archivo Python en una nueva terminal"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems (Linux/Mac)
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
        print("✓ Script ejecutado en una nueva terminal")
    except Exception as e:
        print(f"❌ Ocurrió un error al ejecutar el código: {e}")


def mostrar_menu():
    """Muestra el menú principal del Dashboard"""
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'EjemplosMundoReal_POO',
        '2': 'POO-python'
    }

    while True:
        print(f"\n{'=' * 60}")
        print("   MI DASHBOARD - PROGRAMACIÓN ORIENTADA A OBJETOS ")
        print(f"{'=' * 60}")
        print("1 - 🌍 Ejemplos del Mundo Real")
        print("2 - 🐍 Fundamentos de POO en Python")
        print("0 - 🚪 Salir")
        print(f"{'=' * 60}")

        eleccion_unidad = input("Elige una opción: ")

        if eleccion_unidad == '0':
            print("👋 ¡Hasta luego! Saliendo del programa...")
            break
        elif eleccion_unidad in unidades:
            ruta_unidad = os.path.join(ruta_base, unidades[eleccion_unidad])
            if os.path.exists(ruta_unidad):
                mostrar_sub_menu(ruta_unidad)
            else:
                print(f"❌ La carpeta '{unidades[eleccion_unidad]}' no existe.")
                input("Presiona Enter para continuar...")
        else:
            print("❌ Opción no válida. Por favor, intenta de nuevo.")


def mostrar_sub_menu(ruta_unidad):
    """Muestra subcarpetas Y archivos Python de una unidad"""
    # Obtener subcarpetas Y archivos .py
    try:
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir() and not f.name.startswith('.')]
        archivos_py = [f.name for f in os.scandir(ruta_unidad) if f.is_file() and f.name.endswith('.py')]
    except FileNotFoundError:
        print("❌ La carpeta no existe")
        input("Presiona Enter para regresar...")
        return

    while True:
        print(f"\n{'=' * 60}")
        print("   📂 CONTENIDO DE LA CARPETA")
        print(f"{'=' * 60}")

        # Crear lista de opciones
        opciones = []
        indice = 1

        # Mostrar subcarpetas
        if sub_carpetas:
            print("\n📁 CARPETAS:")
            for carpeta in sub_carpetas:
                print(f"{indice} - 📁 {carpeta}")
                opciones.append(('carpeta', carpeta))
                indice += 1

        # Mostrar archivos Python
        if archivos_py:
            print("\n🐍 ARCHIVOS PYTHON:")
            for archivo in archivos_py:
                print(f"{indice} - 📄 {archivo}")
                opciones.append(('archivo', archivo))
                indice += 1

        # Si no hay contenido
        if not sub_carpetas and not archivos_py:
            print("⚠️  Esta carpeta está vacía.")
            input("Presiona Enter para regresar...")
            break

        print(f"\n0 - ⬅️  Regresar al menú principal")
        print(f"{'=' * 60}")

        eleccion = input("Elige una opción: ")

        if eleccion == '0':
            break
        else:
            try:
                eleccion_idx = int(eleccion) - 1
                if 0 <= eleccion_idx < len(opciones):
                    tipo, nombre = opciones[eleccion_idx]

                    if tipo == 'carpeta':
                        # Navegar a la subcarpeta
                        mostrar_scripts(os.path.join(ruta_unidad, nombre))
                    elif tipo == 'archivo':
                        # Mostrar y ejecutar archivo directamente
                        ruta_script = os.path.join(ruta_unidad, nombre)
                        codigo = mostrar_codigo(ruta_script)
                        if codigo:
                            ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                            if ejecutar == '1':
                                ejecutar_codigo(ruta_script)
                            elif ejecutar == '0':
                                print("ℹ️  No se ejecutó el script.")
                            input("\nPresiona Enter para continuar...")
                else:
                    print("❌ Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("❌ Opción no válida. Por favor, intenta de nuevo.")


def mostrar_scripts(ruta_sub_carpeta):
    """Muestra los scripts Python dentro de una subcarpeta"""
    try:
        scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]
    except FileNotFoundError:
        print("❌ La carpeta no existe")
        input("Presiona Enter para regresar...")
        return

    while True:
        print(f"\n{'=' * 60}")
        print("   📝 SCRIPTS DISPONIBLES")
        print(f"{'=' * 60}")

        if not scripts:
            print("⚠️  No hay archivos Python en esta carpeta.")
            input("Presiona Enter para regresar...")
            break

        # Imprime los scripts
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - 🐍 {script}")

        print(f"\n0 - ⬅️  Regresar al submenú anterior")
        print("9 - 🏠 Regresar al menú principal")
        print(f"{'=' * 60}")

        eleccion_script = input("Elige una opción: ")

        if eleccion_script == '0':
            break
        elif eleccion_script == '9':
            return  # Regresar al menú principal
        else:
            try:
                eleccion_script = int(eleccion_script) - 1
                if 0 <= eleccion_script < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[eleccion_script])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("ℹ️  No se ejecutó el script.")
                        else:
                            print("❌ Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts...")
                else:
                    print("❌ Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("❌ Opción no válida. Por favor, intenta de nuevo.")


# Ejecutar el dashboard
if __name__ == "__main__":
    print("\n Iniciando Dashboard de Programación Orientada a Objetos...\n")
    mostrar_menu()
    print("\n✅ Dashboard cerrado correctamente.\n")