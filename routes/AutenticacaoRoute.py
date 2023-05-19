from fastapi import APIRouter, HTTPException
from fastapi import Body
from models.UsuarioModel import UsuarioLoginModel
from services.AuthService import login_service


router = APIRouter()

@router.post('/login')
async def login(usuario: UsuarioLoginModel = Body(...)):
        resposta = await login_service(usuario)
        if not resposta['status'] == 200:
            raise HTTPException(status_code=resposta['status'], detail=resposta['mensagem'])
        return resposta

