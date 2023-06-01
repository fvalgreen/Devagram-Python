from fastapi import APIRouter, HTTPException, Depends, Header, Body
from middlewares.JWTMiddleware import verificar_token
from models.ComentarioModel import ComentarioCriarModel
from models.PostagemModel import PostagemCriarModel
from services.AuthService import AuthServices
from services.PostagemServices import PostagemServices
from services.UsuarioService import UsuarioServices

router = APIRouter()  # Instanciando o APIRouter no router

postagemService = PostagemServices()
authServices = AuthServices()
usuarioServices = UsuarioServices()


@router.post('/',
             response_description="Rota para criar uma nova postagem",
             dependencies=[Depends(verificar_token)])
async def rota_criar_postagem(Authorization: str = Header(default=''),
                              postagem: PostagemCriarModel = Depends(PostagemCriarModel)):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.criar_postagem(postagem, usuario_logado_id)
        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.get('/',
            response_description="Rota para listar todas as postagem",
            dependencies=[Depends(verificar_token)])
async def rota_listar_todas_postagens():
    try:
        resultado = await postagemService.listar_postagens()
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.get('/seguidos',
            response_description="Rota para listar todas as postagem dos usuários seguidos",
            dependencies=[Depends(verificar_token)])
async def rota_listar_postagens_seguidos(Authorization: str = Header(default='')):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.listar_postagens_seguidos(usuario_logado_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.get('/{usuario_id}',
            response_description="Rota para listar todas as postagem de um usuário específico",
            dependencies=[Depends(verificar_token)])
async def rota_listar_postagens_usuario_especifico(usuario_id: str):
    try:
        resultado = await postagemService.listar_postagens_usuario_especifico(usuario_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.put('/curtir/{postagem_id}',
            response_description="Rota para curtir / descurtir uma postagem",
            dependencies=[Depends(verificar_token)])
async def curtir_descurtir_postagem(postagem_id: str, Authorization: str = Header(default='')):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.curtir_postagem(postagem_id, usuario_logado_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.put('/comentar/{postagem_id}',
            response_description="Rota para comentar uma postagem",
            dependencies=[Depends(verificar_token)])
async def criar_comentario(postagem_id: str,
                           Authorization: str = Header(default=''),
                           comentario_model: ComentarioCriarModel = Body(...)):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.comentar_publicacao(postagem_id, usuario_logado_id,
                                                              comentario_model.comentario)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.delete('/deletar/{postagem_id}',
               response_description="Rota para deletar uma postagem",
               dependencies=[Depends(verificar_token)])
async def deletar_postagem(postagem_id: str,
                           Authorization: str = Header(default='')):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.deletar_postagem(postagem_id, usuario_logado_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.delete('/{postagem_id}/comentario/{comentario_id}',
               response_description="Rota para deletar um comentário",
               dependencies=[Depends(verificar_token)])
async def deletar_comentario(postagem_id: str, comentario_id: str,
                             Authorization: str = Header(default='')):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.deletar_comentario(postagem_id, comentario_id, usuario_logado_id)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro


@router.put('/{postagem_id}/comentario/{comentario_id}',
            response_description="Rota para curtir / descurtir uma postagem",
            dependencies=[Depends(verificar_token)])
async def curtir_descurtir_postagem(postagem_id: str, comentario_id: str, Authorization: str = Header(default=''),
                                    comentario_model: ComentarioCriarModel = Body(...)):
    try:
        usuario_logado_id = authServices.pegar_id_usuario_logado(Authorization)
        resultado = await postagemService.atualizar_comentario(postagem_id,
                                                               comentario_id,
                                                               usuario_logado_id,
                                                               comentario_model.comentario)
        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado
    except Exception as erro:
        raise erro
