from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.PostagemRoute import router as PostagemRoute
from routes.AutenticacaoRoute import router as AutenticacaoRoute
from routes.UsuarioRoute import router as UsuarioRoute

origins = ["*"]

app = FastAPI()

app.include_router(UsuarioRoute, tags=["Usuário"], prefix="/api/usuario")
app.include_router(AutenticacaoRoute, tags=["Login"], prefix="/api/auth")

app.include_router(PostagemRoute, tags=["Postagem"], prefix="/api/postagem")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/api/health', tags=['Health'])
async def health():
    return {
        "status": "Ok!"
    }
