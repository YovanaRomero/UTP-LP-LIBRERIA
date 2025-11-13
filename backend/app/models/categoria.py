from pydantic import BaseModel
from typing import Optional


class CategoriaBase(BaseModel):
    categoria_nombre: str
    categoria_descripcion: str
    categoria_estado: Optional[int] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    categoria_nombre: Optional[str] = None
    categoria_descripcion: Optional[str] = None
    categoria_estado: Optional[int] = None


class Categoria(CategoriaBase):
    categoria_id: int
    categoria_guid: Optional[str] = None

    class Config:
        from_attributes = True
