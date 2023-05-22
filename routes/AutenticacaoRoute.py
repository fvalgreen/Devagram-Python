from fastapi import APIRouter, HTTPException
from fastapi import Body
from models.UsuarioModel import UsuarioLoginModel
from services.AuthService import login_service


router = APIRouter() # Instanciando o APIRouter no router

@router.post('/login') # Definindo o método POST na rota /login desse router
async def login(usuario: UsuarioLoginModel = Body(...)): # Define a função login que receberá do Body as informações
    # seguindo o model UsuarioLoginModel
        resposta = await login_service(usuario) # Passamos para a função service login o usuário a ser logado e
    # guardamos o retorno na variável resposta
        if not resposta['status'] == 200: # Caso o status da resposta não seja 200 nós lançamos uma exception HTTP
            # para informar o que houve de errado
            raise HTTPException(status_code=resposta['status'], detail=resposta['mensagem'])
        return resposta # Caso o status seja 200 retornamos os dados do login

