def revisar_dns(return_data=False):
    try:
        with open('/etc/resolv.conf', 'r') as f:
            lines = f.readlines()
        nameservers = [line.strip().split()[1] for line in lines if line.startswith('nameserver')]
        if return_data:
            return nameservers
        else:
            return "Servidores DNS encontrados:\n" + "\n".join(nameservers)
    except Exception as e:
        return f"Error al leer /etc/resolv.conf: {e}"
