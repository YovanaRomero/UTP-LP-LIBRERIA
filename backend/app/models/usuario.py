from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UsuarioBase(BaseModel):
    usuario_nombre: str
    usuario_descripcion: Optional[str] = None
    usuario_estado: Optional[int] = None

class UsuarioLogin(BaseModel):
    usuario_nombre: str
    usuario_password: str


class Usuario(UsuarioBase):
    usuario_id: int
    usuario_guid: Optional[str] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int
    usuario_nombre: str
    usuario_descripcion: Optional[str] = None
