import os

def usuarios_conectados(return_data=False):
    try:
        output = os.popen("who").read()
        if return_data:
            usuarios = []
            for line in output.strip().split('\n'):
                if line:
                    partes = line.split()
                    usuarios.append({
                        'nombre': partes[0],
                        'origen': partes[-1] if len(partes) > 4 else 'local'
                    })
            return usuarios
        else:
            return output
    except Exception:
        return "No se pudo obtener la lista de usuarios conectados"
