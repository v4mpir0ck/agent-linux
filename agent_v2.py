# Versión 2 del agente IA para Linux
# Guardado el 2025-07-31

import re
from .commands.dns import revisar_dns
from .commands.system import info_sistema, info_cpu, info_memoria, info_discos
from .commands.network import info_interfaces, info_conectividad
from .commands.firewall import estado_firewall
from .commands.process import procesos_top
from .commands.services import estado_servicio
from .commands.users import usuarios_conectados

KEYWORDS = {
    "memoria": ["memoria", "ram", "uso de memoria", "mostrar memoria", "cuanta memoria tengo", "consumo de ram", "quiero ver la memoria", "cuánta ram hay", "estado de la memoria", "ver la ram"],
    "cpu": ["cpu", "procesador", "núcleos", "uso de cpu", "mostrar cpu", "consumo de cpu", "quiero ver la cpu", "estado del procesador", "ver núcleos"],
    "disco": ["disco", "particiones", "espacio libre", "mostrar disco", "almacenamiento", "consumo de disco", "quiero ver el disco", "ver almacenamiento", "estado de los discos"],
    "sistema": ["sistema", "os", "kernel", "versión", "información del sistema", "info sistema", "quiero ver el sistema", "estado del sistema", "ver kernel"],
    "dns": ["dns", "servidores dns", "configuración dns", "mostrar dns", "ver dns", "estado de dns"],
    "red": ["red", "interfaces", "ip", "mostrar red", "estado de red", "conexión de red", "quiero ver la red", "ver interfaces", "estado de la conexión"],
    "conectividad": ["conectividad", "ping", "internet", "conexión", "probar conexión", "test de red", "ver conectividad", "estado de internet"],
    "firewall": ["firewall", "reglas de firewall", "estado del firewall", "mostrar firewall", "ver firewall", "configuración de firewall"],
    "procesos": [
        "procesos", "top", "consumo de procesos", "mostrar procesos", "procesos activos", "ver procesos", "estado de los procesos",
        "consume", "consumo", "más consume", "mas consume", "mayor consumo", "proceso que más consume", "proceso que mas consume"
    ],
    "usuarios": ["usuarios", "conectados", "usuarios conectados", "quién está conectado", "ver usuarios", "estado de usuarios"],
    "servicio": ["servicio", "estado de servicio", "servicio activo", "mostrar servicio", "ver servicio", "estado de un servicio"],
    "ayuda": [
        "ayuda", "help", "qué puedes hacer", "que puedes hacer", "qué sabes hacer", "que sabes hacer",
        "qué más puedes mostrarme", "que mas puedes mostrarme", "qué más puedes hacer", "que mas puedes hacer",
        "opciones", "menú", "mostrar opciones", "mostrar ayuda", "qué comandos hay", "que comandos hay", "qué puedo pedirte", "que puedo pedirte"
    ],
}

def match_keywords(instr, key):
    instr = instr.lower()
    for kw in KEYWORDS[key]:
        if re.search(r"\b" + re.escape(kw) + r"\b", instr):
            return True
    return False

def print_help():
    return (
        "\033[96m🧠  Opciones disponibles:\033[0m\n"
        "🖥️  sistema: Info del sistema operativo\n"
        "🧮  cpu: Info de la CPU\n"
        "💾  memoria: Info de la memoria RAM\n"
        "📀  disco: Info de discos y particiones\n"
        "🌐  red: Info de interfaces de red\n"
        "📡  conectividad: Chequeo de conexión a Internet\n"
        "🛡️  firewall: Estado del firewall\n"
        "📊  procesos: Procesos más consumidores\n"
        "👥  usuarios: Usuarios conectados\n"
        "🔧  servicio <nombre>: Estado de un servicio (ej: servicio sshd)\n"
        "🗂️  dns: Muestra servidores DNS del sistema\n"
        "\nPuedes usar frases naturales como 'quiero ver la memoria', 'estado de la red', 'cuánta ram hay', etc.\n"
        "Para salir: salir, exit, quit.\n"
        "Para ver este menú: ayuda, opciones, qué puedes hacer, etc.\n"
    )

class Agent:
    def handle_instruction(self, instruction: str) -> str:
        instr = instruction.lower()
        # Ayuda
        if match_keywords(instr, "ayuda"):
            return print_help()
        # Procesos: prioriza si la consulta contiene 'cpu' y 'proceso' (singular/plural)
        if match_keywords(instr, "procesos") or ("cpu" in instr and ("proceso" in instr or "procesos" in instr)):
            procesos = procesos_top(return_data=True)
            if "cpu" in instr:
                top_cpu = max(procesos, key=lambda p: p.get("cpu", 0))
                return f"El proceso con mayor uso de CPU es: {top_cpu['nombre']} (PID {top_cpu['pid']}) con {top_cpu['cpu']}%"
            if "memoria" in instr:
                top_mem = max(procesos, key=lambda p: p.get("memoria", 0))
                return f"El proceso con mayor uso de memoria es: {top_mem['nombre']} (PID {top_mem['pid']}) con {top_mem['memoria']} MB"
            if "cuantos" in instr or "cuántos" in instr:
                return f"Hay {len(procesos)} procesos activos."
            resumen = "Procesos activos:\n" + "\n".join([f"{p['nombre']} (PID {p['pid']}) CPU: {p['cpu']}% MEM: {p['memoria']}MB" for p in procesos[:10]])
            return resumen
        # DNS
        if match_keywords(instr, "dns"):
            dns_info = revisar_dns(return_data=True)
            if "cuantos" in instr or "cuántos" in instr:
                return f"Hay {len(dns_info)} servidores DNS configurados."
            return "Servidores DNS configurados:\n" + "\n".join(dns_info)
        # Sistema
        if match_keywords(instr, "sistema"):
            sistema = info_sistema(return_data=True)
            if "kernel" in instr:
                return f"Kernel: {sistema.get('kernel', 'N/A')}"
            if "os" in instr or "sistema operativo" in instr:
                return f"Sistema operativo: {sistema.get('os', 'N/A')}"
            return f"Info sistema: {sistema}"
        # CPU
        if match_keywords(instr, "cpu"):
            cpu = info_cpu(return_data=True)
            if "núcleos" in instr or "cores" in instr:
                return f"Núcleos: {cpu.get('nucleos', 'N/A')}"
            if "uso" in instr or "consumo" in instr:
                return f"Uso actual de CPU: {cpu.get('uso', 'N/A')}%"
            return f"Info CPU: {cpu}"
        # Memoria
        if match_keywords(instr, "memoria"):
            mem = info_memoria(return_data=True)
            if "libre" in instr:
                return f"Memoria libre: {mem.get('libre', 'N/A')} MB"
            if "total" in instr:
                return f"Memoria total: {mem.get('total', 'N/A')} MB"
            if "uso" in instr or "consumo" in instr:
                return f"Uso de memoria: {mem.get('uso', 'N/A')}%"
            return f"Info memoria: {mem}"
        # Disco
        if match_keywords(instr, "disco"):
            discos = info_discos(return_data=True)
            if "libre" in instr:
                libres = [f"{d['nombre']}: {d['libre']} GB libres" for d in discos]
                return "Espacio libre por disco:\n" + "\n".join(libres)
            if "total" in instr:
                totales = [f"{d['nombre']}: {d['total']} GB" for d in discos]
                return "Espacio total por disco:\n" + "\n".join(totales)
            return "Discos y particiones:\n" + "\n".join([f"{d['nombre']} - Total: {d['total']}GB, Libre: {d['libre']}GB" for d in discos])
        # Red
        if match_keywords(instr, "red"):
            redes = info_interfaces(return_data=True)
            if "ip" in instr:
                ips = [f"{r['nombre']}: {r['ip']}" for r in redes]
                return "IPs de interfaces:\n" + "\n".join(ips)
            if "trafico" in instr or "tráfico" in instr:
                top = max(redes, key=lambda r: r.get('trafico', 0))
                return f"La interfaz con más tráfico es {top['nombre']} ({top['trafico']} MB)"
            return "Interfaces de red:\n" + "\n".join([f"{r['nombre']} - IP: {r['ip']}" for r in redes])
        # Conectividad
        if match_keywords(instr, "conectividad"):
            conect = info_conectividad(return_data=True)
            if "internet" in instr or "ping" in instr:
                return f"Conectividad a Internet: {conect.get('internet', 'N/A')}"
            return f"Info conectividad: {conect}"
        # Firewall
        if match_keywords(instr, "firewall"):
            fw = estado_firewall(return_data=True)
            if "activo" in instr or "enabled" in instr:
                return f"Firewall activo: {fw.get('activo', 'N/A')}"
            if "reglas" in instr:
                return "Reglas de firewall:\n" + "\n".join(fw.get('reglas', []))
            return f"Info firewall: {fw}"
        # Usuarios: devuelve lista procesable y permite consultas
        if match_keywords(instr, "usuarios"):
            usuarios = usuarios_conectados(return_data=True)
            if "cuantos" in instr or "cuántos" in instr:
                return f"Hay {len(usuarios)} usuarios conectados."
            if "root" in instr:
                root_users = [u for u in usuarios if u['nombre'] == 'root']
                if root_users:
                    return "El usuario root está conectado."
                else:
                    return "El usuario root no está conectado."
            resumen = "Usuarios conectados:\n" + "\n".join([f"{u['nombre']} desde {u['origen']}" for u in usuarios])
            return resumen
        # Servicios
        if match_keywords(instr, "servicio"):
            partes = instr.split()
            for i, p in enumerate(partes):
                if p == "servicio" and i+1 < len(partes):
                    return estado_servicio(partes[i+1])
            return "Indica el nombre del servicio (ej: servicio sshd)"
        return "Instrucción no reconocida. Opciones: sistema, cpu, memoria, disco, red, conectividad, firewall, procesos, usuarios, servicio <nombre>, dns."
