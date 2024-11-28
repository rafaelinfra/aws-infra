#######################
## Dependências 
#######################

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
from app.createkey import create_or_update_secret


app = FastAPI()

# Servindo arquivos estáticos como o index.html
app.mount("/static", StaticFiles(directory="app/static"), name="static")

#######################
## acessos permitidos -- alterar quando levar para cloud 
#######################
origins = [
    "http://localhost", 
    "http://localhost:8000",  
    "http://127.0.0.1:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["*"],  
)

# Modelo de dados para o usuário
class User(BaseModel):
    email: str
    name: str
    dbname: str
    environment: str
    host: str

# Endpoint para servir a página HTML
@app.get("/", response_class=HTMLResponse)
async def get_html():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# Endpoint para registrar o usuário
@app.post("/register")
async def register_user(user: User):
    password_hash, is_new_user = create_or_update_secret(
        user.email, user.name, user.dbname, user.environment, user.host
    )

    # Se o password_hash foi retornado, verificamos se o usuário é novo
    if is_new_user:
        message = "Usuário registrado com sucesso!"
    else:
        message = "Usuário já existente!"

    # Retorna a resposta com a mensagem e o password_hash
    return {
        "message": message,
        "user": {
            "email": user.email,
            "name": user.name,
            "password_hash": password_hash  # Sempre retornando o password_hash
        }
    }