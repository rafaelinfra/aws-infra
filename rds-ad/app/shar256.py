#######################
## Dependências 
#######################

from base64 import standard_b64encode
from hashlib import pbkdf2_hmac, sha256
from os import urandom
from random import choice
import hmac
import string


salt_size = 16
digest_len = 32
iterations = 4096

#######################
## Gerador de senha aleatória
#######################

def generator_pwd():
    tamanho_da_senha = 12  # Tamanho da senha
    caracteres = string.ascii_letters + string.digits  # Caracteres permitidos (letras e números)
    senha_segura = ''.join(choice(caracteres) for _ in range(tamanho_da_senha))  # Geração da senha
    return senha_segura


# Função para codificar bytes em Base64
def b64enc(b: bytes) -> str:
    return standard_b64encode(b).decode('utf8')


#######################
## Gerador de hash
#######################

def pg_scram_sha256(passwd: str) -> str:
    salt = urandom(salt_size)  # Gera o salt de 16 bytes
    digest_key = pbkdf2_hmac('sha256', passwd.encode('utf8'), salt, iterations, digest_len)
    client_key = hmac.digest(digest_key, 'Client Key'.encode('utf8'), 'sha256')
    stored_key = sha256(client_key).digest()
    server_key = hmac.digest(digest_key, 'Server Key'.encode('utf8'), 'sha256')

    return (
        f'SCRAM-SHA-256${iterations}:{b64enc(salt)}'
        f'${b64enc(stored_key)}:{b64enc(server_key)}'
    )


#######################
## Def Principal
#######################

# def main():
#     # Gera uma senha aleatória
#     senha = generator_pwd()

#     # Gera o hash SCRAM-SHA-256 da senha
#     password_hash = pg_scram_sha256(senha)

#     print(f"Senha gerada: {senha}")
#     print(f"Password Hash: {password_hash}")

# if __name__ == "__main__":
#     main()
