import getpass
import base64
import hashlib
from cryptography.fernet import Fernet

print("=== Generador de token encriptado para Azure OpenAI ===")
token = getpass.getpass("Introduce el token de Azure OpenAI (no se mostrará): ")
passphrase1 = getpass.getpass("Elige una passphrase para proteger el token: ")
passphrase2 = getpass.getpass("Repite la passphrase: ")
if passphrase1 != passphrase2:
    print("[Error] Las passphrases no coinciden. Intenta de nuevo.")
    exit(1)
# Derivar clave Fernet desde passphrase (SHA256, 32 bytes, base64)
key = hashlib.sha256(passphrase1.encode()).digest()[:32]
fernet_key = base64.urlsafe_b64encode(key)
fernet = Fernet(fernet_key)
token_enc = fernet.encrypt(token.encode())
with open("azure_openai_token.enc", "wb") as f:
    f.write(token_enc)
print("\n[OK] Token encriptado guardado en 'azure_openai_token.enc'. Guarda tu passphrase en lugar seguro.")
