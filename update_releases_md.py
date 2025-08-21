import os
from datetime import datetime

RELEASES_MD = "README-releases.md"
HEADER = "# Releases\n\nEste archivo contiene el historial de binarios generados por el pipeline CI/CD.\n\n| Versión | Fecha | Dockerfile | SO/Distro | Enlace Release |\n|---------|-------|------------|-----------|----------------|\n"

def append_release(version, dockerfile, distro, release_url):
    today = datetime.now().strftime("%Y-%m-%d")
    row = f"| {version} | {today} | {dockerfile} | {distro} | [Release]({release_url}) |\n"
    if not os.path.exists(RELEASES_MD):
        with open(RELEASES_MD, "w", encoding="utf-8") as f:
            f.write(HEADER)
    with open(RELEASES_MD, "a", encoding="utf-8") as f:
        f.write(row)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Uso: python update_releases_md.py <version> <dockerfile> <distro> <release_url>")
        sys.exit(1)
    append_release(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
