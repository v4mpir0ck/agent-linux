import platform
import psutil

def info_sistema(return_data=False):
    if return_data:
        return {
            'os': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'hostname': platform.node(),
            'kernel': platform.uname().release
        }
    else:
        return f"Sistema: {platform.system()}\nRelease: {platform.release()}\nVersión: {platform.version()}\nHostname: {platform.node()}\nKernel: {platform.uname().release}"

def info_cpu(return_data=False):
    if return_data:
        return {
            'cpu': platform.processor(),
            'nucleos': psutil.cpu_count(logical=False),
            'hilos': psutil.cpu_count(logical=True),
            'uso': psutil.cpu_percent()
        }
    else:
        return f"CPU: {platform.processor()}\nNúcleos: {psutil.cpu_count(logical=False)}\nHilos: {psutil.cpu_count(logical=True)}\nUso actual: {psutil.cpu_percent()}%"

def info_memoria(return_data=False):
    mem = psutil.virtual_memory()
    if return_data:
        return {
            'total': mem.total // (1024**2),
            'libre': mem.available // (1024**2),
            'uso': mem.percent
        }
    else:
        return f"Memoria total: {mem.total // (1024**2)} MB\nMemoria libre: {mem.available // (1024**2)} MB\nUso: {mem.percent}%"

def info_discos(return_data=False):
    discos = psutil.disk_partitions()
    info = []
    for d in discos:
        uso = psutil.disk_usage(d.mountpoint)
        if return_data:
            info.append({
                'nombre': d.device,
                'montaje': d.mountpoint,
                'total': uso.total // (1024**3),
                'libre': uso.free // (1024**3),
                'usado': uso.percent
            })
        else:
            info.append(f"{d.device} ({d.mountpoint}): {uso.percent}% usado, {uso.free // (1024**3)} GB libres")
    if return_data:
        return info
    else:
        return "\n".join(info)
