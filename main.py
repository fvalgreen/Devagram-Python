from fastapi import FastAPI

from routes.AutenticacaoRoute import router as AutenticacaoRoute
from routes.UsuarioRoute import router as UsuarioRoute

app = FastAPI()

app.include_router(UsuarioRoute, tags=["Usuário"], prefix="/api/cadastro")
app.include_router(AutenticacaoRoute, tags=["Login"], prefix="/api/auth")

@app.get('/api/health', tags=['Health'])

async def health():
    return {
        "status": "Ok!"
    }