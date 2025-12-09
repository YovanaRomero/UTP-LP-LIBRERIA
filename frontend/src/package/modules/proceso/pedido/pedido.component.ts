import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PedidoService } from '../service/pedido.service';
import { ClientePedidoModel } from '../models/cliente.model';
import { PedidoModel } from '../models/pedido.model';
import { HttpErrorResponse } from '@angular/common/http';
import { ButtonModule } from 'primeng/button';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { TableModule } from 'primeng/table';
import { TagModule } from 'primeng/tag';

@Component({
  selector: 'app-pedido',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule,
    AutoCompleteModule,
    TableModule,
    TagModule
  ],
  templateUrl: './pedido.component.html',
  styleUrls: ['./pedido.component.scss'],
})
export class PedidoComponent implements OnInit {
  // VISTA ACTIVA
  vistaActual: 'crear' | 'listar' = 'crear';

  // CARRITO
  carrito: any[] = [];
  subtotal: number = 0;
  igv: number = 0;
  total: number = 0;

  // CLIENTES
  clientes: ClientePedidoModel[] = [];
  clientesFiltrados: ClientePedidoModel[] = [];
  clienteSeleccionado: ClientePedidoModel | null = null;

  // PEDIDOS EXISTENTES
  pedidos: PedidoModel[] = [];
  cargandoPedidos: boolean = false;

  // ESTADOS
  pedidoCreado: boolean = false;
  pedidoNumero: string = '';
  mensajeError: string = '';

  constructor(private pedidoService: PedidoService) { }

  ngOnInit() {
    this.cargarCarrito();
    this.cargarClientes();
    this.cargarPedidos();
  }

  // ==============================
  // CAMBIAR VISTA
  // ==============================
  cambiarVista(vista: 'crear' | 'listar') {
    this.vistaActual = vista;
    if (vista === 'listar') {
      this.cargarPedidos();
    }
  }

  // ==============================
  // LISTAR PEDIDOS
  // ==============================
  cargarPedidos() {
    this.cargandoPedidos = true;
    this.pedidoService.getPedidos().subscribe({
      next: (res: any) => {
        this.pedidos = res;
        console.log('Pedidos cargados:', this.pedidos);
        this.cargandoPedidos = false;
      },
      error: (err: HttpErrorResponse) => {
        console.error('Error al cargar pedidos:', err);
        this.cargandoPedidos = false;
      }
    });
  }

  // ==============================
  // OBTENER ESTADO LABEL Y SEVERITY
  // ==============================
  getEstadoLabel(estado: number | undefined): string {
    if (estado === undefined || estado === null) return 'Desconocido';
    switch (estado) {
      case 1: return 'Pendiente';
      case 2: return 'En Proceso';
      case 3: return 'Entregado';
      case 4: return 'Cancelado';
      default: return 'Desconocido';
    }
  }

  // 🔥 CORRECCIÓN FINAL:
  getEstadoSeverity(estado: number | undefined): "success" | "secondary" | "info" | "warn" | "danger" | "contrast" {
    if (estado === undefined || estado === null) return 'secondary';
    switch (estado) {
      case 1: return 'warn';
      case 2: return 'info';
      case 3: return 'success';
      case 4: return 'danger';
      default: return 'secondary';
    }
  }


  // ==============================
  // CLIENTES
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
        console.log('Clientes cargados:', this.clientes);
      },
      error: () => {
        console.warn('No se pudieron cargar clientes, usando mock.');
        this.clientes = [
          {
            cliente_id: 1,
            nombres: 'Juan',
            apellidos: 'Pérez',
            documento: '12345678',
            correo: 'juan@test.com'
          },
          {
            cliente_id: 2,
            nombres: 'María',
            apellidos: 'García',
            documento: '87654321',
            correo: 'maria@test.com'
          },
          {
            cliente_id: 3,
            nombres: 'Carlos',
            apellidos: 'López',
            documento: '11223344',
            correo: 'carlos@test.com'
          }
        ];
      }
    });
  }

  filtrarClientes(event: any) {
    const query = event.query.toLowerCase();
    if (!query) {
      this.clientesFiltrados = [...this.clientes];
      return;
    }

    this.clientesFiltrados = this.clientes.filter(cliente => {
      const nombreCompleto = `${cliente.nombres} ${cliente.apellidos}`.toLowerCase();
      const documento = cliente.documento.toLowerCase();
      const correo = cliente.correo.toLowerCase();
      return nombreCompleto.includes(query) ||
        documento.includes(query) ||
        correo.includes(query);
    });
  }

  onClienteSelect(event: any) {
    console.log('Cliente seleccionado:', event.value);
    this.clienteSeleccionado = event.value;
    this.mensajeError = '';
  }

  onClienteClear() {
    this.clienteSeleccionado = null;
    console.log('Cliente deseleccionado');
  }

  // ==============================
  // CARRITO
  // ==============================
  cargarCarrito() {
    const data = localStorage.getItem('carrito');
    this.carrito = data ? JSON.parse(data) : [];
    this.actualizarTotales();
  }

  actualizarTotales() {
    this.subtotal = this.carrito.reduce((sum, item) => sum + item.precio * item.cantidad, 0);
    this.igv = this.subtotal * 0.18;
    this.total = this.subtotal + this.igv;
  }

  eliminarProducto(index: number) {
    this.carrito.splice(index, 1);
    localStorage.setItem('carrito', JSON.stringify(this.carrito));
    this.actualizarTotales();
  }

  cambiarCantidad(item: any) {
    if (item.cantidad < 1) item.cantidad = 1;
    localStorage.setItem('carrito', JSON.stringify(this.carrito));
    this.actualizarTotales();
  }

  // ==============================
  // CREAR PEDIDO
  // ==============================
  crearPedido() {
    this.mensajeError = '';
    this.pedidoCreado = false;

    if (!this.clienteSeleccionado || !this.clienteSeleccionado.cliente_id) {
      this.mensajeError = 'Debe seleccionar un cliente válido.';
      return;
    }

    if (this.carrito.length === 0) {
      this.mensajeError = 'El carrito está vacío.';
      return;
    }

    const body = {
      cliente_cliente_id: this.clienteSeleccionado.cliente_id,
      pedido_subtotal: this.subtotal,
      pedido_igv: this.igv,
      pedido_total: this.total,
      pedido_observaciones: "Pedido desde Angular",
      detalles: this.carrito.map(item => ({
        detalle_producto_id: item.id,
        detalle_cantidad: item.cantidad
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
        this.clienteSeleccionado = null;

        console.log('Pedido creado exitosamente:', res);

        // Recargar lista de pedidos
        this.cargarPedidos();
      },
      error: (err: HttpErrorResponse) => {
        console.error('Error al crear pedido:', err);
        this.mensajeError = err.error?.message || err.error?.detail || 'Error al crear pedido.';
      }
    });
  }
}