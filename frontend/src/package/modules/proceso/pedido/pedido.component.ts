import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PedidoService } from '../service/pedido.service';
import { ClientePedidoModel } from '../models/cliente.model';
import { HttpErrorResponse } from '@angular/common/http';
import { ButtonModule } from 'primeng/button';
@Component({
  selector: 'app-pedido',
  standalone: true,
  imports: [CommonModule, FormsModule,ButtonModule],
  templateUrl: './pedido.component.html',
  styleUrls: ['./pedido.component.scss'],
})
export class PedidoComponent {

  carrito: any[] = [];
  subtotal: number = 0;
  igv: number = 0;
  total: number = 0;

  clientes: ClientePedidoModel[] = [];
  clienteSeleccionado: number | null = null;

  pedidoCreado: boolean = false;
  pedidoNumero: string = '';
  mensajeError: string = '';

  constructor(private pedidoService: PedidoService) {}

  ngOnInit() {
    this.cargarCarrito();
    this.cargarClientes();
  }

  // ==============================
  //         CLIENTES
  // ==============================
  cargarClientes() {
    this.pedidoService.getClientes().subscribe({
      next: (res: any[]) => {
        this.clientes = res.map(c => ({
          cliente_id: c.cliente_id,
          nombres: c.cliente_nombres,
          apellidos: c.cliente_apellidos,
          documento: c.cliente_dni,
          correo: c.cliente_correo
        }));
      },
      error: () => {
        console.warn('No se pudieron cargar clientes, usando mock.');
        this.clientes = [
          { cliente_id: 1, nombres: 'Juan', apellidos: 'Pérez', documento: '12345678', correo: 'juan@test.com' }
        ];
      }
    });
  }

  // ==============================
  //         CARRITO
  // ==============================
  cargarCarrito() {
    const data = localStorage.getItem('carrito');
    this.carrito = data ? JSON.parse(data) : [];
    this.actualizarTotales();
  }

  actualizarTotales() {
    this.subtotal = this.carrito.reduce((sum, item) => sum + item.precio * item.cantidad, 0);
    this.igv = this.subtotal * 0.18; // IGV 18%
    this.total = this.subtotal + this.igv;
  }

  // ==============================
  //         CREAR PEDIDO
  // ==============================
  crearPedido() {
    this.mensajeError = '';
    this.pedidoCreado = false;

    if (!this.clienteSeleccionado) {
      this.mensajeError = 'Debe seleccionar un cliente.';
      return;
    }

    if (this.carrito.length === 0) {
      this.mensajeError = 'El carrito está vacío.';
      return;
    }

    const body = {
      cliente_cliente_id: Number(this.clienteSeleccionado),
      pedido_subtotal: this.subtotal,
      pedido_igv: this.igv,
      pedido_total: this.total,
      productos: this.carrito.map(item => ({
        producto_id: item.id,
        cantidad: item.cantidad
      }))
    };

    console.log('Payload pedido:', body);

    this.pedidoService.createPedido(body).subscribe({
      next: (res: any) => {
        this.pedidoCreado = true;
        this.pedidoNumero = res.pedido_numero ?? 'SIN NUMERO';
        localStorage.removeItem('carrito');
        this.carrito = [];
        this.subtotal = 0;
        this.igv = 0;
        this.total = 0;
      },
      error: (err: HttpErrorResponse) => {
        console.error('Error al crear pedido', err);
        this.mensajeError = err.error?.message || 'Error al crear pedido.';
      }
    });
  }



  // ==============================
  // Eliminar producto del carrito
  // ==============================
  eliminarProducto(index: number) {
  this.carrito.splice(index, 1);      // elimina del array
  localStorage.setItem('carrito', JSON.stringify(this.carrito)); // actualiza localStorage
  this.actualizarTotales();            // recalcula subtotal, IGV y total
  }

  // ==============================
  //         ACTUALIZAR CANTIDAD
  // ==============================
  cambiarCantidad(item: any) {
    if (item.cantidad < 1) item.cantidad = 1;
    this.actualizarTotales();
  }

}
