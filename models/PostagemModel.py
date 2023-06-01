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
    curtidas: List = Field(...)
    comentarios: List = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "id": "string",
                "usuario_id": "string",
                "foto": "string",
                "legenda": "string",
                "data": "Date",
                "curtidas": "List",
                "comentarios": "List"
            }
        }


@decoratorUtil.form_body
class PostagemCriarModel(BaseModel):
    foto: UploadFile = Field(...)
    legenda: str = Field(...)

    class Config:
        schema_extra = {
            "postagem": {
                "legenda": "string",
            }
        }
