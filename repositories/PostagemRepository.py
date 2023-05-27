from datetime import datetime
from bson import ObjectId
import motor.motor_asyncio
from decouple import config
from models.PostagemModel import PostagemCriarModel
from utils.ConverterUtil import ConverterUtil

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.dbDevagramPython

postagem_collection = database.get_collection("postagem")

converterUtil = ConverterUtil()


class PostagemRepository:
    async def criar_postagem(self, legenda, usuario_id) -> dict:
        nova_postagem_dict = {
            "usuario_id": ObjectId(usuario_id),
            "legenda": legenda,
            "curtidas": [],
            "comentarios": [],
            "data": datetime.now(),
            "foto": ""
        }


        postagem_criada = await postagem_collection.insert_one(nova_postagem_dict)

        nova_postagem = await postagem_collection.find_one({"_id": postagem_criada.inserted_id})

        return converterUtil.postagem_converter(nova_postagem)

    async def listar_postagens(self):
        postagens_encontradas = postagem_collection.aggregate([{
            "$lookup": {
                "from": "usuarios",
                "localField": "usuario_id",
                "foreignField": "_id",
                "as": "usuario"
            }
        }])

        postagens = []

        async for postagem in postagens_encontradas:
            postagens.append(converterUtil.postagem_converter(postagem))
            index = 0
            postagens[0]["usuario"]["senha"] = ''

        return postagens


    async def listar_postagens_usuario(self, id):
        return postagem_collection.find({"usuario": id})

    async def buscar_postagem_pelo_id(self, idPostagem: str) -> dict:
        postagem = await postagem_collection.find_one({"_id": ObjectId(idPostagem)})

        if postagem:
            return converterUtil.postagem_converter(postagem)

    async def deletar_postagem(self, idPostagem: str):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if postagem:
            await postagem_collection.delete_one({"_id": ObjectId(id)})

    async def atualizar_postagem(self, id: str, dados_postagem: dict):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if postagem:
            await postagem_collection.update_one({"_id": ObjectId(id)}, {"$set": dados_postagem})

            postagem_atualizada = await postagem_collection.find_one({"_id": ObjectId(id)})

            return converterUtil.postagem_converter(postagem_atualizada)

