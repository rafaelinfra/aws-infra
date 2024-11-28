#######################
## Dependências 
#######################

import boto3
import json
import os
from dotenv import load_dotenv
from app.shar256 import pg_scram_sha256, generator_pwd

load_dotenv()

#######################
## Iniciando o client de conexão com a AWS
#######################

client = boto3.client('secretsmanager',
                    verify=False,
                    aws_access_key_id=(os.environ["AWS_ACCESS"]),
                    aws_secret_access_key=(os.environ["AWS_SECRET"]),
                    region_name=(os.environ["REGION"])
                    )

#######################
## Função responsável por consultar a existência do 
## usuário no AWS Secret Manager e caso não ele cria com algumas informações importantes
## Retorno com False para Segredo já existente, e True para necessidade de criação
#######################

def create_or_update_secret(email, name, dbname, environment, host):

    secret_name_to_check = f"{name}_{environment}"  
    
    try:        
        response = client.get_secret_value(SecretId=secret_name_to_check)
        secret_value = json.loads(response['SecretString'])
        password_hash = secret_value.get('password_hash')
        return password_hash, False  
    except client.exceptions.ResourceNotFoundException:
        
        senha = generator_pwd()  # Gera uma senha
        password_hash = pg_scram_sha256(senha)  # Gera o hash da senha
        
        secret_value = {
            "email_usuario": email,
            "nome_usuario": name,
            "ambiente": environment,
            "banco_de_dados": dbname,
            "host": host,
            "password_hash": password_hash,
            "senha": senha  
        }

        ## Cria o segredo utilizando o json (secret_value)
        create_response = client.create_secret(
            Name=secret_name_to_check,
            Description="Segredo criado via aplicação",
            SecretString=json.dumps(secret_value)
        )
        return password_hash, True 
