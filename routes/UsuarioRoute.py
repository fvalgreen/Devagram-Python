import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from middlewares.JWTMiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from services.AuthService import AuthServices
from services.UsuarioService import UsuarioServices

router = APIRouter()  # Instanciando o APIRouter no router

usuarioServices = UsuarioServices()
authServices = AuthServices()


@router.post('/',
             response_description="Rota para criar um novo usuário")  # Definindo o método POST na rota / desse  router
async def rota_criar_usuario(file: UploadFile, usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):  # Definindo
    # uma função
    # assincrona a ser executada na rota. Ela recebe um usuario que vem do Body como parametro
    caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}'

    with open(caminho_foto, 'wb+') as arquivo:
        arquivo.write(file.file.read())

    resultado = await usuarioServices.registrar_usuario(usuario, caminho_foto)  # Usa o usuário que veio no body da
    # request como
    # parametro da função
    # registrar usuário e guarda o resultado num variável


    os.remove(caminho_foto)

    if not resultado['status'] == 201:  # Se o status dentro da dict resultado não for igual a 201 é levantado uma
        # exception dizendo qual foi o status retornado pela aplicação e qual erro aconteceu

        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
    return resultado  # Caso tenha dado tudo certo retorna o resultado


@router.get('/me', response_description="Rota para receber os dados do usuário logado", dependencies=[Depends(
    verificar_token)])
async def buscar_dados_usuario_logado(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = authServices.decodificar_token_jwt(token)

        resultado = await usuarioServices.buscar_usuario(payload['usuario_id'])

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.get('/{usuario_id}', response_description="Rota para receber os dados do usuário por id", dependencies=[Depends(
    verificar_token)])
async def buscar_dados_usuario_id(usuario_id: str, Authorization: str = Header(default='')):
    try:

        resultado = await usuarioServices.buscar_usuario(usuario_id)

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.get('/filtrar/{nome}', response_description="Rota para receber os dados do usuário por filtro", dependencies=[
    Depends(
    verificar_token)])
async def buscar_dados_usuario_filtro(nome: str, Authorization: str = Header(default='')):
    try:

        resultado = await usuarioServices.buscar_usuario_filtro(nome)

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.get('/', response_description="Rota para listar todos os usuários", dependencies=[Depends(
    verificar_token)])
async def listar_usuarios():
    try:

        resultado = await usuarioServices.buscar_todos_usuario()

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")



@router.put('/me', response_description="Rota para atualizar os dados do usuário logado", dependencies=[Depends(
    verificar_token)])
async def atualizar_dados_usuario_logado(file: UploadFile, Authorization: str = Header(default=''),
                                         usuario_atualizar: UsuarioAtualizarModel =
                                         Depends(UsuarioAtualizarModel)):
    try:
        caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}'

        with open(caminho_foto, 'wb+') as arquivo:
            arquivo.write(file.file.read())

        token = Authorization.split(' ')[1]
        payload = authServices.decodificar_token_jwt(token)

        resultado = await usuarioServices.atualizar_usuario_logado(payload['usuario_id'], usuario_atualizar,
                                                                   caminho_foto)

        os.remove(caminho_foto)

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

@router.put('/seguir/{usuario_seguir_id}', response_description="Rota para seguir um usuário",
            dependencies=[Depends(
    verificar_token)])
async def seguir_usuario(usuario_seguir_id: str ,Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = authServices.decodificar_token_jwt(token)

        resultado = await usuarioServices.seguir_usuario(payload["usuario_id"], usuario_seguir_id)

        if not resultado['status'] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
        return resultado
    except Exception as erro:
        print(erro)
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
