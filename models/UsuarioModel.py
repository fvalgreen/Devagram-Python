from typing import List

from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


@decoratorUtil.form_body
class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string",
                "email": "string",
                "senha": "string",
                "avatar": "string",

            }
        }


class UsuarioModel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    avatar: str = Field(...)
    seguidores: List = Field(...)
    seguindo: List = Field(...)
    publicacoes: int = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "id": "string",
                "nome": "string",
                "email": "string",
                "senha": "string",
                "avatar": "string",
                "seguidores": "List",
                "seguindo": "List",
                "publicacoes": "int"
            }
        }


class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "email": "string",
                "senha": "string"
            }
        }


@decoratorUtil.form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "string"
            }
        }
