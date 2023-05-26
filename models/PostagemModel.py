from typing import List
from fastapi import UploadFile
from pydantic import BaseModel, Field

from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario_id: str = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str = Field(...)
    curtidas: int = Field(...)
    comentarios: List = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "id": "dsfasfdasdfa",
                "usuario_id": "id do usuário",
                "foto": "foto.png",
                "legenda": "Foto de fulano",
                "data": "25/05/2023",
                "curtidas": 0,
                "comentarios": "List[comentarios]"
            }
        }


@decoratorUtil.form_body
class PostagemCriarModel(BaseModel):
    foto: UploadFile = Field(...)
    legenda: str = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "legenda": "Foto de fulano",
            }
        }
