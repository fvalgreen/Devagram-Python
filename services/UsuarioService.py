from models.UsuarioModel import UsuarioCriarModel
from repositories.UsuarioRepository import (
    criar_usuario,
    buscar_usuario_por_email,
    listar_usuarios,
    deletar_usuario,
    atualizar_usuario
)


async def registrar_usuario(usuario: UsuarioCriarModel): # Cria a função de registrar o usuário
    try:
        usuario_encontrado = await buscar_usuario_por_email(usuario.email) # busca o usuário na DB pelo email

        if usuario_encontrado: # Caso retorne algum usuário com esse e-amil dá um erro informando que o e-mail já
            # está cadastrado no sistema
            return {
                "mensagem": f'E-mail  {usuario.email} já está cadastrado no sistema',
                "dados": "",
                "status": 400
            }
        else: # Caso não retorne nenhum usuário com esse e-mail cria o usuário passando os dados
            novo_usuario = await criar_usuario(usuario)
            novo_usuario["senha"] = "" # define a senha como uma string vazia para não retorna a senha do usuário

            return{ # Retorna uma mensagem de sucesso e os dados do usuário
                "mensagem": "Usuário cadastrado com sucesso",
                "dados": novo_usuario,
                "status": 201
            }
    except Exception as error:
        return {
            "mensagem": "Erro interno no servidor",
            "dados": str(error),
            "status": 500

        }