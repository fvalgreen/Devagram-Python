from typing import List
from pydantic import BaseModel, Field

from models.ComentarioModel import ComentarioModel
from models.UsuarioModel import UsuarioModel


class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario: UsuarioModel = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: int = Field(...)
    comentarios: List[ComentarioModel] = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "id": "dsfasfdasdfa",
                "usuario": "UsuarioModel",
                "foto": "foto.png",
                "legenda": "Foto de fulano",
                "data": "25/05/2023",
                "curtidas": 0,
                "comentarios": "List[comentarios]"
            }
        }

class PostagemCriarModel(BaseModel):
    usuario: UsuarioModel = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)


    class Config:
        schema_extra = {
            "postagem": {
                "usuario": "UsuarioModel",
                "foto": "foto.png",
                "legenda": "Foto de fulano",
            }
        }