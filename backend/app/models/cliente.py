from pydantic import BaseModel
from typing import Optional


class ClienteBase(BaseModel):
    cliente_dni: str
    cleinte_nombres: str
    cliente_apellidos: str
    cliente_direccion: Optional[str] = None
    cliente_distrito: Optional[str] = None
    cliente_correo: Optional[str] = None
    cliente_celular: Optional[str] = None
    cliente_estado: Optional[int] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    cliente_dni: Optional[str] = None
    cleinte_nombres: Optional[str] = None
    cliente_apellidos: Optional[str] = None
    cliente_direccion: Optional[str] = None
    cliente_distrito: Optional[str] = None
    cliente_correo: Optional[str] = None
    cliente_celular: Optional[str] = None
    cliente_estado: Optional[int] = None


class Cliente(ClienteBase):
    cliente_id: int
    cliente_guid: Optional[str] = None

    class Config:
        from_attributes = True
