import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from middlewares.JWTMiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel
from services.AuthService import decodificar_token_jwt
from services.UsuarioService import (registrar_usuario, buscar_usuario)

router = APIRouter()  # Instanciando o APIRouter no router


@router.post('/',
             response_description="Rota para criar um novo usuário")  # Definindo o método POST na rota / desse  router
async def rotaCriarUsuario(file: UploadFile, usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):  # Definindo uma função
    # assincrona a ser executada na rota. Ela recebe um usuario que vem do Body como parametro
    caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}'

    with open(caminho_foto, 'wb+') as arquivo:
        arquivo.write(file.file.read())

    resultado = await registrar_usuario(usuario, caminho_foto)  # Usa o usuário que veio no body da request como
    # parametro da função
    # registrar usuário e guarda o resultado num variável

    os.remove(caminho_foto)

    if not resultado['status'] == 201:  # Se o status dentro da dict resultado não for igual a 201 é levantado uma
       # exception dizendo qual foi o status retornado pela aplicação e qual erro aconteceu

      raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
    return resultado  # Caso tenha dado tudo certo retorna o resultado



@router.get('/me', response_description="Rota para receber os dados do usário logado", dependencies=[Depends(
    verificar_token)])
async def buscar_dados_usuario_logado(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = decodificar_token_jwt(token)

        resultado = await buscar_usuario(payload['usuario_id'])

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
