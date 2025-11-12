from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    categoria_descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    categoria_descripcion: Optional[str] = None

class Categoria(CategoriaBase):
    categoria_id: int

    class Config:
        from_attributes = True
