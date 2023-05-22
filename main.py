from fastapi import FastAPI
from routes.AutenticacaoRoute import router as AutenticacaoRoute
from routes.UsuarioRoute import router as UsuarioRoute

app = FastAPI() #Instanciando o FastAPI no app

app.include_router(UsuarioRoute, tags=["Usuário"], prefix="/api/cadastro") # incluindo a rota de cadastro no app na rota /api/cadastro
app.include_router(AutenticacaoRoute, tags=["Login"], prefix="/api/auth") # incluindo a rota de login no app na rota /api/cadsatro

@app.get('/api/health', tags=['Health']) # Definindo uma rota chamada Helath para testar se o servidor está ok

async def health():
    return {
        "status": "Ok!"
    }