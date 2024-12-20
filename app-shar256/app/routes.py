#######################
## Dependências 
#######################

from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.info_rds_awsconfig import rds_list  # Importa a função existente
from app.my_msal import get_access_token, get_msal_app
from app.createkey import create_or_update_secret
from dotenv import load_dotenv
from app.basemodel import User
import os

load_dotenv()

router = APIRouter()

# Função para verificar se o usuário está autenticado
def check_authentication(request: Request):
    token = request.cookies.get("access_token")  # Verificando o token no cookie
    if not token:
        raise HTTPException(status_code=401, detail="Não autenticado. Faça login primeiro.")
    return token

# Endpoint página HTML
@router.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    try:
        token = check_authentication(request)
    except HTTPException:
        return RedirectResponse(url="/login")  # Redireciona para o login caso não autenticado

    with open("app/static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content, status_code=200)

# Endpoint para registrar o usuário
@router.post("/register")
async def register_user(user: User):
    password_hash, is_new_user = create_or_update_secret(
        # user.email, user.name, user.dbname, user.environment, user.host
        user.email, user.name, user.dbname, user.host, user.version
    )

    message = "Usuário registrado com sucesso!" if is_new_user else "Usuário já existente!"

    return {
        "message": message,
        "user": {
            "email": user.email,
            "name": user.name,
            "password_hash": password_hash
        }
    }


@router.get("/consult-rds")
async def consult_rds():
    try:
        data = rds_list()
        return data.to_dict(orient="records")  # Retorna a tabela como JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar bancos: {str(e)}")

# Função de login e redirecionamento para Azure AD
@router.get("/login")
async def login():
    msal_app = get_msal_app()

    auth_url = msal_app.get_authorization_request_url(
        scopes=os.getenv("SCOPE", "").split(","),
        redirect_uri=os.getenv("REDIRECT_URI")
    )
    
    return RedirectResponse(auth_url)

# Endpoint de callback após o login
@router.get("/auth/callback")
async def auth_callback(code: str):
    try:
        access_token = get_access_token(code)
        
        response = RedirectResponse(url="/")
        response.set_cookie(key="access_token", value=access_token, httponly=False, max_age=3600)
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na autenticação: {str(e)}")
