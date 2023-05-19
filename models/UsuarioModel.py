from pydantic import BaseModel, Field, EmailStr

class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    avatar: str = Field(...)
    seguidores: int = Field(...)
    seguindo: int = Field(...)
    publicacoes: int = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "id": "dsfasfdasdfa",
                "nome": "Fulano",
                "email": "fulano@gmail.com",
                "senha": "Senha@123",
                "avatar": "fulano.png",
                "seguidores": 0,
                "seguindo": 0,
                "publicacoes": 0
            }
        }

class UsuarioModel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    avatar: str = Field(...)
    seguidores: int = Field(...)
    seguindo: int = Field(...)
    publicacoes: int = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "Fulano",
                "email": "fulano@gmail.com",
                "senha": "Senha@123",
                "avatar": "fulano.png",
                "seguidores": 0,
                "seguindo": 0,
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