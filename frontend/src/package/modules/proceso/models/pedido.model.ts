import { DetalleModel } from './detalle.model';

export interface PedidoRequest {
  cliente_cliente_id: number;
  pedido_subtotal: number;
  pedido_igv: number;
  pedido_total: number;
  pedido_estado?: number;
  pedido_observaciones?: string;
  detalles: {
    detalle_producto_id: number;
    detalle_cantidad: number;
  }[];
}

export interface PedidoModel {
  pedido_id?: number;
  pedido_guid?: string;
  pedido_numero?: string;
  pedido_fecha_registro?: string;
  pedido_fecha_entrega?: string;
  pedido_personal_delivery?: string;
  pedido_observaciones?: string;
  cliente_cliente_id: number;
  pedido_subtotal: number;
  pedido_igv: number;
  pedido_total: number;
  pedido_estado?: number;
}