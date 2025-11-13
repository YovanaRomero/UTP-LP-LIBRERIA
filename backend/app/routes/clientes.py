from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Cliente, ClienteCreate, ClienteUpdate
from ..services import ClienteService

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/", response_model=List[Cliente], status_code=status.HTTP_200_OK)
def listar_clientes():
    """Listar todos los clientes"""
    clientes = ClienteService.get_all_clientes()
    return clientes


@router.get("/{cliente_id}", response_model=Cliente, status_code=status.HTTP_200_OK)
def obtener_cliente(cliente_id: int):
    """Obtener un cliente por ID"""
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    return cliente


@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteCreate):
    """Crear un nuevo cliente"""
    nuevo_cliente = ClienteService.create_cliente(cliente)
    if nuevo_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el cliente"
        )
    return nuevo_cliente


@router.put("/{cliente_id}", response_model=Cliente, status_code=status.HTTP_200_OK)
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    """Actualizar un cliente existente"""
    cliente_actualizado = ClienteService.update_cliente(cliente_id, cliente)
    if cliente_actualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    return cliente_actualizado


@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK)
def eliminar_cliente(cliente_id: int):
    """Eliminar un cliente"""
    eliminado = ClienteService.delete_cliente(cliente_id)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    return {"message": f"Cliente con ID {cliente_id} eliminado correctamente"}
