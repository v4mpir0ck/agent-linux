import psutil
import socket
import os

def info_interfaces(return_data=False):
    info = []
    for name, addrs in psutil.net_if_addrs().items():
        ips = [a.address for a in addrs if a.family == socket.AF_INET]
        if return_data:
            info.append({'nombre': name, 'ip': ips[0] if ips else 'N/A'})
        else:
            info.append(f"{name}: {', '.join(ips)}")
    if return_data:
        return info
    else:
        return "\n".join(info)

def info_conectividad(return_data=False):
    response = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1")
    if return_data:
        return {'internet': 'OK' if response == 0 else 'ERROR'}
    else:
        return "Conectividad: OK" if response == 0 else "Conectividad: ERROR"
