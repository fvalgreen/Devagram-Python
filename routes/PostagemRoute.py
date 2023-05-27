from fastapi import APIRouter, HTTPException, Depends, Header
from middlewares.JWTMiddleware import verificar_token
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

        # resultado_usuario = await usuarioServices.buscar_usuario(payload["usuario_id"])

        # usuario = resultado["dados"]

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
