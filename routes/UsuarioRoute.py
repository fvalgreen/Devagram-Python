from fastapi import APIRouter, HTTPException
from fastapi import Body
from models.UsuarioModel import UsuarioCriarModel
from services.UsuarioService import ( registrar_usuario)


router = APIRouter() # Instanciando o APIRouter no router

@router.post('/', response_description="Rota para criar um novo usuário") # Definindo o método POST na rota / desse  router

async def rotaCriarUsuario(usuario: UsuarioCriarModel = Body(...)): # Definindo uma função assincrona a ser executada
    # na rota. Ela recebe um usuario que vem do Body como parametro
    resultado = await registrar_usuario(usuario) # Usa o usuário que veio no body da request como parametro da função
    # registrar usuário e guarda o resultado num variável

    if not resultado['status'] == 201: # Se o status dentro da dict resultado não for igual a 201 é levantado uma
        # exception dizendo qual foi o status retornado pela aplicação e qual erro aconteceu
        raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])
    return resultado # Caso tenha dado tudo certo retorna o resultado
