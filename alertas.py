import psutil
import subprocess

def diagnostico_sistema():
    datos = {}
    # CPU
    datos['cpu'] = {'usage': psutil.cpu_percent(interval=1)}
    # Memoria
    mem = psutil.virtual_memory()
    datos['memoria'] = {'usage': mem.percent}
    # Disco (root)
    disk = psutil.disk_usage('/')
    datos['disco'] = {'free_pct': 100 - disk.percent, 'mount': '/'}
    # Red
    net_status = 'estable'
    try:
        subprocess.check_output('ping -c 1 -W 2 8.8.8.8', shell=True)
    except Exception:
        net_status = 'inestable'
    datos['red'] = {'status': net_status}
    # NTP
    ntp_enabled = True
    try:
        out = subprocess.check_output('timedatectl show -p NTPSynchronized', shell=True, universal_newlines=True)
        ntp_enabled = 'yes' in out.lower() or 'true' in out.lower()
    except Exception:
        ntp_enabled = False
    datos['ntp'] = {'enabled': ntp_enabled}
    # Actualizaciones (solo para sistemas apt)
    updates_pending = False
    try:
        out = subprocess.check_output('apt list --upgradable 2>/dev/null | grep -v "Listing..."', shell=True, universal_newlines=True)
        updates_pending = bool(out.strip())
    except Exception:
        updates_pending = False
    datos['updates'] = {'pending': updates_pending}
    return datos
def sugerir_alertas(problemas):
    # problemas: lista de strings con problemas detectados
    alertas = []
    for problema in problemas:
        if 'memoria' in problema:
            alertas.append('Posible falta de RAM, revisar procesos y swap.')
        elif 'disco' in problema:
            alertas.append('Espacio en disco bajo, liberar espacio o ampliar.')
        elif 'cpu' in problema:
            alertas.append('CPU alta, revisar procesos consumidores.')
        elif 'red' in problema:
            alertas.append('Problemas de red, comprobar conectividad y configuración.')
        else:
            alertas.append(f'Revisar: {problema}')
    return '\n'.join(alertas)


def mostrar_alertas():
    datos = diagnostico_sistema()
    return generar_alertas_desde_diagnostico(datos)


def generar_alertas_desde_diagnostico(datos):
    """
    Recibe un dict con resultados de diagnóstico y genera alertas clasificadas.
    Ejemplo de datos:
    {
        'cpu': {'usage': 95},
        'memoria': {'usage': 88},
        'disco': {'free_pct': 7, 'mount': '/var'},
        'red': {'status': 'inestable'},
        'ntp': {'enabled': False},
        'updates': {'pending': True}
    }
    """
    alertas = []
    # Disco
    if 'disco' in datos and datos['disco'].get('free_pct', 100) < 10:
        alertas.append({
            "mensaje": f"Espacio en disco bajo en {datos['disco'].get('mount','?')}",
            "nivel": "critico",
            "sugerencia": "Libera espacio o amplía el disco."
        })
    # CPU
    if 'cpu' in datos and datos['cpu'].get('usage', 0) > 90:
        alertas.append({
            "mensaje": "Uso de CPU elevado (>90%)",
            "nivel": "warning",
            "sugerencia": "Revisa procesos consumidores."
        })
    # Memoria
    if 'memoria' in datos and datos['memoria'].get('usage', 0) > 85:
        alertas.append({
            "mensaje": "Uso de memoria RAM elevado (>85%)",
            "nivel": "warning",
            "sugerencia": "Revisa procesos y swap."
        })
    # Red
    if 'red' in datos and datos['red'].get('status') == 'inestable':
        alertas.append({
            "mensaje": "Conexión de red inestable",
            "nivel": "warning",
            "sugerencia": "Verifica cables y configuración de red."
        })
    # NTP
    if 'ntp' in datos and not datos['ntp'].get('enabled', True):
        alertas.append({
            "mensaje": "Sincronización NTP deshabilitada",
            "nivel": "info",
            "sugerencia": "Activa el servicio NTP para mantener la hora."
        })
    # Actualizaciones
    if 'updates' in datos and datos['updates'].get('pending', False):
        alertas.append({
            "mensaje": "Actualizaciones de seguridad pendientes",
            "nivel": "info",
            "sugerencia": "Ejecuta el gestor de actualizaciones."
        })
    return alertas
