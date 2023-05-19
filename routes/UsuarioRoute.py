from fastapi import APIRouter, HTTPException
from fastapi import Body
from models.UsuarioModel import UsuarioCriarModel
from services.UsuarioService import ( registrar_usuario)


router = APIRouter()

@router.post('/', response_description="Rota para criar um novo usuário")

async def rotaCriarUsuario(usuario: UsuarioCriarModel = Body(...)):
    resultado = await registrar_usuario(usuario)

    if not resultado['status'] == 201:
        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
    return resultado