
from bson import ObjectId
import motor.motor_asyncio
from decouple import config
from models.UsuarioModel import UsuarioCriarModel
from utils.AuthUtil import gerar_senha_criptografada

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.dbDevagramPython

usuario_collection = database.get_collection("usuarios")

def usuario_helper(usuario): # define uma função helper que pega o usuário e transforma numa dict

    return {
        "id": str(usuario["_id"]),
        "nome": usuario['nome'],
        "email": usuario['email'],
        "senha": usuario['senha'],
        "avatar": usuario['avatar'] if 'avatar' in usuario else '',
        "seguidores": usuario['seguidores'],
        "seguindo": usuario['seguindo'],
        "publicacoes": usuario['publicacoes']
    }

async def criar_usuario(usuario: UsuarioCriarModel) -> dict: # cria a função de criar o usuário na DB
    # A função recebe um usuário com o model UsuarioCriarModel
    usuario.senha = gerar_senha_criptografada(usuario.senha) # Criptografa a senha do usuário para guardar no DB
    usuario_criado = await usuario_collection.insert_one(usuario.__dict__) # guarda o usuário no DB como uma dict
    # O insert_one retorna um ID
    novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id}) # Buscando o usuário no DB
    # usando esse ID

    return usuario_helper(novo_usuario) # Retorna esse usuário usando o helper para transformar ele numa dict

async def listar_usuarios(): # Cria a funçãoo de buscar usuário
    return usuario_collection.find() #Dá um find sem parametros ns DB para buscar todos os usuários

async def buscar_usuario_por_id(id: str) -> dict:
    usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

    if usuario:
        return usuario_helper(usuario);

async def buscar_usuario_por_email(email: str) -> dict: #Cria a função de buscar usuário por email
    usuario = await usuario_collection.find_one({"email": email}) #Dá um find_one ns DB passando como parametro o
    # email do usuário informado

    if usuario: # Caso haja um usuário com esse email na DB retorna ele usando o helper
        return usuario_helper(usuario)


async def atualizar_usuario(id: str, dados_usuario: dict): # Cria a função de atualizar os dados do usuário,
    # recebendo como parametros o id do usuário a ser atualizado e os dados a serem atualizados
    usuario = await usuario_collection.find_one({"_id": ObjectId(id)}) # Busca o usuário na DB usando o ID

    if usuario: # Caso retorne um usuário com esse id
        usuario_atualizado = await usuario_collection.update_one({"_id": ObjectId(id)}, {"$set": dados_usuario}) #
        # atualiza os dados na DB passando o id e os dados a serem alterados
        usuario_atualizado = await usuario_collection.find_one({"_id": ObjectId(id)})

        return usuario_helper(usuario_atualizado) #retorna o usuário atualizado usando o helper

async def deletar_usuario(id: str): # Cria a função de deletar um usuário
    usuario = await usuario_collection.find_one({"_id": ObjectId(id)}) # busca na DB o usuário pelo ID

    if usuario: # Caso haja um usuário com esse ID remove ele da DB
        await usuario_collection.delete_one({"_id": ObjectId(id)})