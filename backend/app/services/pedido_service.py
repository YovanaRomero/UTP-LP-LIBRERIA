from typing import List
from decimal import Decimal
from datetime import datetime
from fastapi import HTTPException

from ..models import Pedido, PedidoCreate, PedidoUpdate, DetalleCreate
from ..repositories.pedido_repository import PedidoRepository
from ..repositories.cliente_repository import ClienteRepository
from ..repositories.producto_repository import ProductoRepository
from ..repositories.detalle_repository import DetalleRepository


class PedidoService:
    IGV_RATE = Decimal("0.18")

    # ===========================
    # VALIDAR CLIENTE EXISTE
    # ===========================
    @staticmethod
    def validar_cliente(cliente_id: int) -> bool:
        return ClienteRepository.get_by_id(cliente_id) is not None

    # ===========================
    # VALIDAR PRODUCTOS Y STOCK
    # ===========================
    @staticmethod
    def validar_productos(detalles: List[DetalleCreate]):
        errores = []
        productos_validos = []

        for d in detalles:
            producto = ProductoRepository.get_by_id(d.detalle_producto_id)

            if not producto:
                errores.append(f"Producto con ID {d.detalle_producto_id} no existe.")
                continue

            if producto.producto_stock < d.detalle_cantidad:
                errores.append(
                    f"Stock insuficiente para producto {producto.producto_nombre}. "
                    f"Solicitado: {d.detalle_cantidad}, Disponible: {producto.producto_stock}"
                )
                continue

            productos_validos.append(producto)

        if errores:
            raise HTTPException(status_code=400, detail=errores)

        return productos_validos

    # ===========================
    # CALCULAR MONTOS
    # ===========================
    @staticmethod
    def calcular_subtotal(detalles: List[DetalleCreate], productos: list) -> Decimal:
        subtotal = Decimal("0.00")
        for d, p in zip(detalles, productos):
            subtotal += Decimal(str(p.producto_precio)) * d.detalle_cantidad
        return subtotal

    @staticmethod
    def calcular_igv(subtotal: Decimal) -> Decimal:
        return (subtotal * PedidoService.IGV_RATE).quantize(Decimal("0.01"))

    @staticmethod
    def calcular_total(subtotal: Decimal, igv: Decimal) -> Decimal:
        return (subtotal + igv).quantize(Decimal("0.01"))

    # ===========================
    # CREAR PEDIDO
    # ===========================
    @staticmethod
    def create(pedido_in: PedidoCreate):
        # 1) Validar cliente
        if not PedidoService.validar_cliente(pedido_in.cliente_cliente_id):
            raise HTTPException(status_code=404, detail="El cliente no existe.")

        # 2) Validar productos y stock
        productos_validos = PedidoService.validar_productos(pedido_in.detalles)

        # 3) Calcular montos
        subtotal = PedidoService.calcular_subtotal(pedido_in.detalles, productos_validos)
        igv = PedidoService.calcular_igv(subtotal)
        total = PedidoService.calcular_total(subtotal, igv)

        # 4) Completar campos calculados
        pedido_in.pedido_subtotal = float(subtotal)
        pedido_in.pedido_igv = float(igv)
        pedido_in.pedido_total = float(total)
        pedido_in.pedido_estado = pedido_in.pedido_estado or 1  # Registrado

        # 5) Crear pedido en BD
        pedido_creado = PedidoRepository.create(pedido_in)
        if not pedido_creado:
            raise HTTPException(status_code=500, detail="No se pudo crear el pedido.")

        # 6) Crear detalles y actualizar stock
        for i, (d, p) in enumerate(zip(pedido_in.detalles, productos_validos), start=1):
            detalle_data = DetalleCreate(
                detalle_producto_id=d.detalle_producto_id,
                detalle_producto_precio=float(p.producto_precio),
                detalle_cantidad=d.detalle_cantidad,
                detalle_secuencia=i
            )
            # Crear detalle
            DetalleRepository.create(pedido_creado.pedido_id, detalle_data, i)

            # Descontar stock
            ProductoRepository.descontar_stock(p.producto_id, d.detalle_cantidad)

        return pedido_creado

    # ===========================
    # OBTENER PEDIDO POR ID
    # ===========================
    @staticmethod
    def get_by_id(pedido_id: int):
        pedido = PedidoRepository.get_by_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        return pedido

    # ===========================
    # LISTAR TODOS LOS PEDIDOS
    # ===========================
    @staticmethod
    def get_all():
        return PedidoRepository.get_all()

    # ===========================
    # ACTUALIZAR PEDIDO
    # ===========================
    @staticmethod
    def update(pedido_id: int, pedido_in: PedidoUpdate):
        pedido_actualizado = PedidoRepository.update(pedido_id, pedido_in)
        if not pedido_actualizado:
            raise HTTPException(status_code=404, detail="Pedido no encontrado o no actualizado.")
        return pedido_actualizado

    # ===========================
    # ELIMINAR PEDIDO
    # ===========================
    @staticmethod
    def delete(pedido_id: int):
        exito = PedidoRepository.delete(pedido_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Pedido no encontrado o no eliminado.")
        return {"message": "Pedido eliminado correctamente."}

    # ===========================
    # BUSCAR PEDIDOS POR DNI CLIENTE
    # ===========================
    @staticmethod
    def buscar_por_dni_cliente(dni: str):
        cliente = ClienteRepository.get_by_dni(dni)
        if not cliente:
            return []
        return PedidoRepository.get_by_cliente(cliente.cliente_id)

    # ===========================
    # BUSCAR PEDIDOS POR DNI DELIVERY
    # ===========================
    @staticmethod
    def buscar_por_dni_delivery(dni_delivery: str):
        return PedidoRepository.get_by_delivery(dni_delivery)

    # ===========================
    # BUSCAR PEDIDOS POR RANGO DE FECHAS
    # ===========================
    @staticmethod
    def buscar_por_rango_fechas(desde_str: str, hasta_str: str):
        try:
            desde = datetime.strptime(desde_str, "%Y-%m-%d").date()
            hasta = datetime.strptime(hasta_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")
        return PedidoRepository.get_by_rango_fechas(desde, hasta)

    # ===========================
    # REGISTRAR ENTREGA
    # ===========================
    @staticmethod
    def registrar_entrega(pedido_id: int, fecha_entrega_str: str, observaciones: str):
        pedido = PedidoRepository.get_by_id(pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")

        try:
            fecha_entrega = datetime.strptime(fecha_entrega_str, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD.")

        update = PedidoUpdate(
            pedido_fecha_entrega=fecha_entrega,
            pedido_observaciones=observaciones,
            pedido_estado=2  # Entregado
        )

        pedido_actualizado = PedidoRepository.update(pedido_id, update)
        if not pedido_actualizado:
            raise HTTPException(status_code=500, detail="No se pudo registrar la entrega.")

        return pedido_actualizado