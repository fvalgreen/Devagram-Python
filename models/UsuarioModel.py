from typing import List

from pydantic import BaseModel, Field, EmailStr
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


@decoratorUtil.form_body
class UsuarioCriarModel(BaseModel):  # Criando uma classe UsuarioCriarModel que herda as propriedades da classe
    # BaseModel
    nome: str = Field(...)  # Definindo a propriedade nome do tipo string
    email: EmailStr = Field(...)  # Definimos a propriedade email do tipo Emailstr do Pydantic
    senha: str = Field(...)  # Definindo a propriedade senha do tipo string


    class Config:  # Criando a class config para servir como exemplo na documentação da api
        schema_extra = {
            "usuario": {  # define que a class UsuarioCriarModel espera um usuário com as seguintes propriedades
                "nome": "Fulano",
                "email": "fulano@gmail.com",
                "senha": "Senha@123",
                "avatar": "fulano.png",

            }
        }


class UsuarioModel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    avatar: str = Field(...)
    seguidores: List = Field(...)  # Definindo a propriedade seguidores do tipo inteiro
    seguindo: List = Field(...)  # Definindo a propriedade seguindo do tipo inteiro
    publicacoes: int = Field(...)  # Definindo a propriedade publicações do tipo inteiro

    class Config:
        schema_extra = {
            "usuario": {
                "id": "bdnyudbgf67dsf89gdfs32897hrg",
                "nome": "Fulano",
                "email": "fulano@gmail.com",
                "senha": "Senha@123",
                "avatar": "fulano.png",
                "seguidores": [],
                "seguindo": [],
                "publicacoes": 0
            }
        }


class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "email": "fulano@gmail.com",
                "senha": "Senha@123"
            }
        }


@decoratorUtil.form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)

    # Caso precise atualizar mais dados é só inserir aqui
    class Config:
        schema_extra = {
            "usuario": {
                "nome": "Fulano"
            }
        }
