import { DetalleModel } from './detalle.model';

export interface PedidoRequest {
  cliente_cliente_id: number;
  pedido_subtotal: number;
  pedido_igv: number;
  pedido_total: number;
  pedido_estado?: number; // 1 = activo
  pedido_observaciones?: string;
  productos: {
    producto_id: number;
    cantidad: number;
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