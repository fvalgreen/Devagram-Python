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
        token = Authorization.split(" ")[1]
        payload = authServices.decodificar_token_jwt(token)

        resultado = await postagemService.criar_postagem(postagem, payload['usuario_id'])

        if not resultado["status"] == 201:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        return resultado

    except Exception as erro:
        raise erro


@router.get('/',
            response_description="Rota para criar uma nova postagem",
            dependencies=[Depends(verificar_token)])
async def rota_criar_postagem():
    try:
        resultado = await postagemService.listar_postagens()

        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        return resultado

    except Exception as erro:
        raise erro


@router.put('/curtir/{postagem_id}',
            response_description="Rota para curtir / descriptive uma postagem",
            dependencies=[Depends(verificar_token)])
async def curtir_descurtir_postagem(postagem_id: str, Authorization: str = Header(default='')):
    try:
        token = Authorization.split(" ")[1]
        payload = authServices.decodificar_token_jwt(token)

        resultado = await postagemService.curtir_postagem(postagem_id, payload["usuario_id"])

        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
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
        token = Authorization.split(" ")[1]
        payload = authServices.decodificar_token_jwt(token)

        resultado = await postagemService.comentar_publicacao(postagem_id, payload["usuario_id"],
                                                              comentario_model.comentario)

        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado["status"], detail=resultado["mensagem"])
        return resultado

    except Exception as erro:
        raise erro
