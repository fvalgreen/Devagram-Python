import time
import jwt
from decouple import config

from dtos.ReturnDto import ReturnDto
from models.UsuarioModel import UsuarioLoginModel
from repositories.UsuarioRepository import UsuarioRepository
from utils.AuthUtil import AuthUtils

JWT_SECRET = config('JWT_SECRET')

usuarioRepository = UsuarioRepository()
authUtils = AuthUtils()


class AuthServices:

    @staticmethod
    def gerar_token_jwt(usuario_id: str) -> str:

        payload = {
            "usuario_id": usuario_id,
            "expires": time.time() + 6000
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return token

    @staticmethod
    def decodificar_token_jwt(token: str):
        try:
            token_decodificado = jwt.decode(token, JWT_SECRET,
                                            algorithms="HS256")

            if token_decodificado["expires"] >= time.time():
                return token_decodificado
            else:
                return None
        except Exception:
            return None

    def pegar_id_usuario_logado(self, authorization):
        token = authorization.split(' ')[1]
        payload = self.decodificar_token_jwt(token)
        return payload["usuario_id"]

    async def login_service(self,
                            usuario: UsuarioLoginModel):
        usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

        if not usuario_encontrado:
            return ReturnDto("Email ou Senha incorreto", "", 400)
        else:
            if authUtils.verificar_senha(usuario.senha, usuario_encontrado['senha']):
                usuario_encontrado[
                    'senha'] = ''
                token = self.gerar_token_jwt(
                    usuario_encontrado["id"])
                usuario_encontrado["token"] = token

                return ReturnDto("Login realizado com sucesso", usuario_encontrado, 200)

            else:
                return ReturnDto("Email ou Senha incorreto", "", 400)
