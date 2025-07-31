def revisar_dns():
    try:
        with open('/etc/resolv.conf', 'r') as f:
            lines = f.readlines()
        nameservers = [line.strip() for line in lines if line.startswith('nameserver')]
        return "Servidores DNS encontrados:\n" + "\n".join(nameservers)
    except Exception as e:
        return f"Error al leer /etc/resolv.conf: {e}"
