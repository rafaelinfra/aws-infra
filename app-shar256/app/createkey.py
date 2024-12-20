from app.shar256 import pg_scram_sha256, generator_pwd, pg_md5_hash
from dotenv import load_dotenv
import boto3
import json
import os

load_dotenv()

client = boto3.client('secretsmanager',
                    verify=False,
                    aws_access_key_id=(os.environ["AWS_ACCESS"]),
                    aws_secret_access_key=(os.environ["AWS_SECRET"]),
                    region_name=(os.environ["REGION"])
                    )

def create_or_update_secret(email, name, dbname, host, version):
    secret_name_to_check = f"{name}/{dbname}"  
    
    try:        
        response = client.get_secret_value(SecretId=secret_name_to_check)
        secret_value = json.loads(response['SecretString'])
        password_hash = secret_value.get('password_hash')
        return password_hash, False  
    
    except client.exceptions.ResourceNotFoundException:
        senha = generator_pwd()  # Gera uma senha
        # Verifica a versão e escolhe o algoritmo de hash adequado
        version_float = float(version)
        if version_float < 14:
            password_hash = pg_md5_hash(name, senha)  # Gera o hash MD5
        else:
            password_hash = pg_scram_sha256(senha)  # Gera o hash SHA-256
        
        secret_value = {
            "userEmail": email,
            "username": name,
            "DatabaseName": dbname,
            "host": host,
            "password_hash": password_hash,
            "password": senha,
            "EngineVersion": version,

        }

        create_response = client.create_secret(
            Name=secret_name_to_check,
            Description="Segredo criado via aplicação",
            SecretString=json.dumps(secret_value)
        )
        return password_hash, True