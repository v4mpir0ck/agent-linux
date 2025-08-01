import psutil

def procesos_top(return_data=False):
    procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:10]
    if return_data:
        return [
            {
                'pid': p.info['pid'],
                'nombre': p.info['name'],
                'cpu': p.info['cpu_percent'],
                'memoria': round(p.info['memory_percent'], 2)
            }
            for p in procs
        ]
    else:
        return "\n".join([f"{p.info['pid']} {p.info['name']} CPU: {p.info['cpu_percent']}% MEM: {p.info['memory_percent']}%" for p in procs])
