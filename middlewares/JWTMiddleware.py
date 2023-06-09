from fastapi import Header, HTTPException

from services.AuthService import AuthServices

authServices = AuthServices()


async def verificar_token(Authorization: str = Header(default='')):
    if not Authorization.split(' ')[0] == 'Bearer':
        raise HTTPException(status_code=401, detail="Necessário Token para autenticação")
    token = Authorization.split(' ')[1]
    payload = authServices.decodificar_token_jwt(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return payload
