#######################
## Dependências 
#######################

from dotenv import load_dotenv
import msal
import os

load_dotenv()


# Variáveis de configuração do Azure AD
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = os.getenv("SCOPE", "").split(",")  # Dividir os escopos por vírgula

# MSAL App
def get_msal_app():
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )

# token de acesso
def get_access_token(auth_code: str):
    msal_app = get_msal_app()

    result = msal_app.acquire_token_by_authorization_code(
        auth_code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI,
    )

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Erro ao obter token: {result.get('error_description')}")
