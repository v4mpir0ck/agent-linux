import os

def mostrar_configuracion(archivos=None):
    if archivos is None:
        archivos = ['/etc/ssh/sshd_config', '/etc/fstab', '/etc/resolv.conf']
    resultado = []
    for archivo in archivos:
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
            resultado.append(f"--- {archivo} ---\n{contenido}\n{'-'*40}")
        else:
            resultado.append(f"No existe: {archivo}\n{'-'*40}")
    return '\n'.join(resultado)

def comparar_configuracion(archivo1, archivo2):
    if not os.path.exists(archivo1) or not os.path.exists(archivo2):
        return "Uno o ambos archivos no existen."
    with open(archivo1, 'r', encoding='utf-8', errors='ignore') as f1, open(archivo2, 'r', encoding='utf-8', errors='ignore') as f2:
        contenido1 = f1.readlines()
        contenido2 = f2.readlines()
    import difflib
    diff = difflib.unified_diff(contenido1, contenido2, fromfile=archivo1, tofile=archivo2)
    return '\n'.join(diff)
