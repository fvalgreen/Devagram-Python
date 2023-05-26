
from bson import ObjectId
import motor.motor_asyncio
from decouple import config
from models.UsuarioModel import UsuarioCriarModel
from utils.AuthUtil import AuthUtils
from utils.ConverterUtil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.dbDevagramPython

usuario_collection = database.get_collection("usuarios")

converterUtil = ConverterUtil()
authUtils = AuthUtils()


class UsuarioRepository:
    @staticmethod
    async def criar_usuario(usuario: UsuarioCriarModel) -> dict:  # cria a função de criar o usuário na DB
        # A função recebe um usuário com o model UsuarioCriarModel
        usuario.senha = authUtils.gerar_senha_criptografada(usuario.senha)  # Criptografa a senha do usuário para
        # guardar no DB
        usuario_criado = await usuario_collection.insert_one(usuario.__dict__)  # guarda o usuário no DB como uma dict
        # O insert_one retorna um ID
        novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})  # Buscando o usuário
        # no DB
        # usando esse ID

        return converterUtil.usuario_converter(novo_usuario)  # Retorna esse usuário usando o helper para transformar
        # ele numa dict

    @staticmethod
    async def listar_usuarios():  # Cria a funçãoo de buscar usuário
        return usuario_collection.find()  # Dá um find sem parametros ns DB para buscar todos os usuários

    @staticmethod
    async def buscar_usuario_por_id(id: str) -> dict:
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            return converterUtil.usuario_converter(usuario)

    @staticmethod
    async def buscar_usuario_por_email(email: str) -> dict:  # Cria a função de buscar usuário por email
        usuario = await usuario_collection.find_one({"email": email})  # Dá um find_one ns DB passando como parametro o
        # email do usuário informado

        if usuario:  # Caso haja um usuário com esse email na DB retorna ele usando o helper
            return converterUtil.usuario_converter(usuario)

    @staticmethod
    async def atualizar_usuario(id: str, dados_usuario: dict):  # Cria a função de atualizar os dados do usuário,
        # recebendo como parametros o id do usuário a ser atualizado e os dados a serem atualizados
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})  # Busca o usuário na DB usando o ID

        if usuario:  # Caso retorne um usuário com esse id
            await usuario_collection.update_one({"_id": ObjectId(id)}, {"$set": dados_usuario})
            # atualiza os dados na DB passando o id e os dados a serem alterados
            usuario_atualizado = await usuario_collection.find_one({"_id": ObjectId(id)})

            return converterUtil.usuario_converter(usuario_atualizado)  # retorna o usuário atualizado usando o helper

    @staticmethod
    async def deletar_usuario(id: str):  # Cria a função de deletar um usuário
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})  # busca na DB o usuário pelo ID

        if usuario:  # Caso haja um usuário com esse ID remove ele da DB
            await usuario_collection.delete_one({"_id": ObjectId(id)})
