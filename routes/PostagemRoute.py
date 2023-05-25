import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from middlewares.JWTMiddleware import verificar_token
from models.PostagemModel import PostagemCriarModel
from models.UsuarioModel import UsuarioCriarModel

router = APIRouter()  # Instanciando o APIRouter no router


@router.post('/',
             response_description="Rota para criar uma nova postagem")
async def rotaCriarPostagem(file: UploadFile, postagem: PostagemCriarModel = Depends(PostagemCriarModel)):

    caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}'

    with open(caminho_foto, 'wb+') as arquivo:
        arquivo.write(file.file.read())

    # resultado = await registrar_usuario(usuario, caminho_foto)

    os.remove(caminho_foto)
    return {"teste": "OK!"}




@router.get('/', response_description="Rota para listar as postagens", dependencies=[Depends(
    verificar_token)])
async def listar_postagens(Authorization: str = Header(default='')):
    try:
       return { "teste": "OK!"}
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.get('/me', response_description="Rota para listar as postagens do usuário", dependencies=[Depends(
    verificar_token)])
async def buscar_dados_usuario_logado(Authorization: str = Header(default='')):
    try:
       return { "teste": "OK!"}
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")