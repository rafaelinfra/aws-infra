#######################
## Dependências 
#######################


from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routes import router
import uvicorn
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do FastAPI
app = FastAPI()

# Servindo arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configuração CORS
origins = [
    "*",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["*"],  
)

# Incluir as rotas
app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
