
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
    async def criar_usuario(usuario: UsuarioCriarModel) -> dict:
        usuario.senha = authUtils.gerar_senha_criptografada(usuario.senha)
        usuario_dict = {
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
            "seguidores": [],
            "seguindo": [],
            "publicacoes": 0
        }

        usuario_criado = await usuario_collection.insert_one(usuario_dict)
        novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})
        novo_usuario_formatado = converterUtil.usuario_converter(novo_usuario)
        novo_usuario_formatado["senha"] = ""
        return novo_usuario_formatado

    @staticmethod
    async def listar_usuarios():

        usuarios_encontrados = usuario_collection.find()
        usuarios = []

        async for usuario in usuarios_encontrados:
            usuarios.append(converterUtil.usuario_converter(usuario))

        return usuarios

    @staticmethod
    async def buscar_usuario_por_id(id: str) -> dict:
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            return converterUtil.usuario_converter(usuario)

    @staticmethod
    async def buscar_usuario_por_filtro(nome: str):

        usuarios_encontrados = usuario_collection.find({
            "nome": {
                "$regex": nome,
                '$options': 'i'
            }
        })

        usuarios = []

        async for usuario in usuarios_encontrados:
            usuarios.append(converterUtil.usuario_converter(usuario))

        return usuarios

    @staticmethod
    async def buscar_usuario_por_email(email: str) -> dict:
        usuario = await usuario_collection.find_one({"email": email})

        if usuario:
            return converterUtil.usuario_converter(usuario)

    @staticmethod
    async def atualizar_usuario(id: str, dados_usuario: dict):
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            await usuario_collection.update_one({"_id": ObjectId(id)}, {"$set": dados_usuario})

            usuario_atualizado = await usuario_collection.find_one({"_id": ObjectId(id)})

            return converterUtil.usuario_converter(usuario_atualizado)

    @staticmethod
    async def deletar_usuario(id: str):
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            await usuario_collection.delete_one({"_id": ObjectId(id)})
