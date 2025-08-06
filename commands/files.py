import os

# Comando: Cambiar hostname

def cambiar_hostname(nuevo_hostname):
    # Simulación: en producción usaría 'os.system' o editar /etc/hostname
    return f"Hostname cambiado a: {nuevo_hostname} (simulación)"

# Comando: Buscar fichero por nombre

def buscar_fichero(nombre, base_path="."):
    for root, dirs, files in os.walk(base_path):
        if nombre in files:
            return os.path.join(root, nombre)
    return None

# Comando: Leer entradas de un fichero

def leer_fichero(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error al leer el fichero: {e}"

# Comando: Añadir entrada a un fichero

def añadir_a_fichero(path, texto):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(texto + "\n")
        return f"Entrada añadida a {path} (simulación)"
    except Exception as e:
        return f"Error al escribir en el fichero: {e}"
