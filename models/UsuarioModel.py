from pydantic import BaseModel, Field, EmailStr

class UsuarioCriarModel(BaseModel): #Criando uma classe UsuarioCriarModel que herda as propriedades da classe BaseModel
    nome: str = Field(...) # Definindo a propriedade nome do tipo string
    email: EmailStr = Field(...) # Definimos a propriedade email do tipo Emailstr do Pydantic
    senha: str = Field(...) # Definindo a propriedade senha do tipo string
    avatar: str = Field(...) # Definindo a propriedade avatar do tipo string
    seguidores: int = Field(...) # Definindo a propriedade seguidores do tipo inteiro
    seguindo: int = Field(...) # Definindo a propriedade seguindo do tipo inteiro
    publicacoes: int = Field(...) # Definindo a propriedade publicações do tipo inteiro

    class Config: # Criando a class config para servir como exemplo na documentação da api
        schema_extra = {
            "usuario": { # define que a class UsuarioCriarModel espera um usuário com as seguintes propriedades
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