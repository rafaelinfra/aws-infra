import boto3
import sys
import os
from dotenv import load_dotenv

load_dotenv()

## Inicia a sessão baseada nas variáveis de ambiente

def delete_secret(secretname):
    client = boto3.client('secretsmanager',
                        verify=False,
                        aws_access_key_id=(os.environ["AWS_ACCESS"]),
                        aws_secret_access_key=(os.environ["AWS_SECRET"]),
                        region_name=(os.environ["REGION"])
                        )

    response = client.delete_secret(
        SecretId=secretname,
        ForceDeleteWithoutRecovery=True
    )

def main():
    args = sys.argv[1:]

    if args and len(args) > 1:
        print_usage()

    if args:
        secretname = args[0]
    else:
        secretname = sys.stdin.read().strip()

    if not secretname:
        print_usage()

    print(delete_secret(secretname))

if __name__ == "__main__":
    main()