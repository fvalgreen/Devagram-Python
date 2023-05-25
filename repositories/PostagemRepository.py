import datetime
from bson import ObjectId
import motor.motor_asyncio
from decouple import config
from models.PostagemModel import PostagemCriarModel

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.dbDevagramPython

postagem_collection = database.get_collection("postagem")

def postagem_helper(postagem):
    return {
        "id": str(postagem["_id"]),
        "usuario": postagem["usuario"],
        "foto": postagem["foto"],
        "legenda": postagem["legenda"],
        "data": postagem["data"],
        "curtidas": postagem["curtidas"],
        "comentarios": postagem["comentarios"]
    }

async def criar_postagem(postagem: PostagemCriarModel) -> dict:
    postagem_a_ser_criada = postagem
    postagem_a_ser_criada["data"] = datetime.date.today()
    postagem_a_ser_criada["curtidas"] = 0
    postagem_a_ser_criada["comentarios"] = []
    postagem_criada = await postagem_collection.insert_one(postagem.__dict__)

    nova_postagem = await postagem_collection.find_one({"_id": postagem_criada.inserted_id})

    return postagem_helper(nova_postagem)

async def listar_postagens():
    return postagem_collection.find()

async def buscar_postagem_pelo_id(id: str) -> dict:
    postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

    if postagem:
        return postagem_helper(postagem)

async def deletar_postagem(id: str):
    postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

    if postagem:
        await postagem_collection.delete_one({"_id": ObjectId(id)})

