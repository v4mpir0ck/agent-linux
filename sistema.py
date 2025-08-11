import platform

def info_sistema():
    return f"Sistema operativo: {platform.system()}\nVersión: {platform.version()}\nRelease: {platform.release()}\nMachine: {platform.machine()}"
