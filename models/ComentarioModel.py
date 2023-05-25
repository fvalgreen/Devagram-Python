from pydantic import BaseModel, Field

from models.UsuarioModel import UsuarioModel


class ComentarioModel(BaseModel):
    usuario: UsuarioModel = Field(...)
    comentario: str = Field(...)