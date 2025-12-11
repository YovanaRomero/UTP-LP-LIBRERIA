import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ConfirmationService } from 'primeng/api';
import { MessageService } from 'primeng/api';
import { BlockUI } from 'primeng/blockui';
import { ButtonModule } from 'primeng/button';
import { SelectModule } from 'primeng/select';
import { ChipModule } from 'primeng/chip';
import { DialogModule } from 'primeng/dialog';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { InputTextModule } from 'primeng/inputtext';
import { Table, TableModule } from 'primeng/table';
import { TextareaModule } from 'primeng/textarea';
import { ToastModule } from 'primeng/toast';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { MessageModule } from 'primeng/message';

import { ProductoModel } from '@/shared/models/producto.model';
import { ProductoService } from '@/shared/service/producto.service';
import { CategoriaService } from '@/shared/service/categoria.service';
import { CategoriaModel } from '@/shared/models/categoria.model';

@Component({
  selector: 'app-producto',
  standalone: true,
  imports: [
    FormsModule,
    ToastModule,
    TableModule,
    ChipModule,
    ButtonModule,
    DialogModule,
    ConfirmDialogModule,
    CommonModule,
    InputTextModule,
    TextareaModule,
    ToggleSwitchModule,
    SelectModule,
    MessageModule
  ],
  providers: [ConfirmationService, MessageService],
  templateUrl: './producto.component.html',
  styleUrls: ['./producto.component.scss'],
})
export class ProductoComponent implements OnInit {

  @ViewChild('dt') dt!: Table;

  isLoading: boolean = true;
  productos: ProductoModel[] = [];
  productoDialog: boolean = false;
  producto: ProductoModel = {} as ProductoModel;
  selectedProductos: ProductoModel[] = [];
  submitted: boolean = false;
  isEditMode: boolean = false;
  loading: boolean = false;

  estados = [
    { label: 'Activo', value: 1 },
    { label: 'Inactivo', value: 0 }
  ];

  categorias: CategoriaModel[] = [];

  constructor(
    private productoService: ProductoService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService
    , private categoriaService: CategoriaService
  ) {}

  ngOnInit(): void {
    this.loadProductos();
    this.loadCategorias();
  }

  loadCategorias(): void {
    this.categoriaService.getAll().subscribe({
      next: (data) => {
        this.categorias = data || [];
      },
      error: () => {
        this.messageService.add({
          severity: 'warn',
          summary: 'Aviso',
          detail: 'No se pudieron cargar las categorías, intente más tarde',
          life: 3000
        });
      }
    });
  }

  loadProductos(): void {
    this.loading = true;
    this.productoService.getAll().subscribe({
      next: (data) => {
        this.productos = data;
        this.loading = false;
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los productos',
          life: 3000
        });
        this.loading = false;
      }
    });
  }

  getChip(estado: number): string {
    switch (estado) {
      case 0: return 'chip-inactivo';
      case 1: return 'chip-activo';
      default: return 'chip-default';
    }
  }

  openNew(): void {
    this.producto = {} as ProductoModel;
    this.producto.producto_estado = 1;
    this.submitted = false;
    this.isEditMode = false;
    this.productoDialog = true;
  }

  editProducto(producto: ProductoModel): void {
    this.producto = { ...producto };
    this.isEditMode = true;
    this.productoDialog = true;
  }

  hideDialog(): void {
    this.productoDialog = false;
    this.submitted = false;
  }

  deleteProducto(producto: ProductoModel): void {
    this.confirmationService.confirm({
      message: `¿Está seguro de eliminar el producto ${producto.producto_nombre}?`,
      header: 'Confirmar',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        if (producto.producto_id) {
          this.productoService.delete(producto.producto_id).subscribe({
            next: () => {
              this.productos = this.productos.filter(c => c.producto_id !== producto.producto_id);
              this.messageService.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Producto eliminado correctamente',
                life: 3000
              });
            },
            error: () => {
              this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudo eliminar el producto',
                life: 3000
              });
            }
          });
        }
      }
    });
  }

  saveProducto(): void {
    this.submitted = true;
    if (this.producto.producto_nombre?.trim() && this.producto.producto_descripcion?.trim()) {
      if (this.isEditMode && this.producto.producto_id) {
        this.productoService.update(this.producto.producto_id, this.producto).subscribe({
          next: (data) => {
            const index = this.productos.findIndex(c => c.producto_id === data.producto_id);
            if (index !== -1) this.productos[index] = data;
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: 'Producto actualizado correctamente',
              life: 3000
            });
            this.productoDialog = false;
            this.producto = {} as ProductoModel;
          },
          error: () => this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'No se pudo actualizar el producto',
            life: 3000
          })
        });
      } else {
        this.productoService.create(this.producto).subscribe({
          next: (data) => {
            this.productos.push(data);
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: 'Producto creado correctamente',
              life: 3000
            });
            this.productoDialog = false;
            this.producto = {} as ProductoModel;
          },
          error: () => this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'No se pudo crear el producto',
            life: 3000
          })
        });
      }
    }
  }

  // ==============================
  // AGREGAR AL CARRITO
  // ==============================
  agregarAlCarrito(producto: ProductoModel) {
    const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');

    const existe = carrito.find((p: any) => p.id === producto.producto_id);
    if (existe) {
      existe.cantidad += 1;
    } else {
      carrito.push({
        id: producto.producto_id,
        nombre: producto.producto_nombre,
        precio: producto.producto_precio,
        cantidad: 1
      });
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));
    this.messageService.add({
      severity: 'success',
      summary: 'Éxito',
      detail: `${producto.producto_nombre} agregado al carrito`,
      life: 2000
    });
  }
  descargarExcel() {
    this.productoService.exportarExcel().subscribe({
      next: (response) => {
        const blob = new Blob([response.body as BlobPart], {
          type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        });
  
        const url = window.URL.createObjectURL(blob);
  
        const a = document.createElement('a');
        a.href = url;
  
        // Si quieres leer el filename enviado desde FastAPI:
        const contentDisposition = response.headers.get('Content-Disposition');
        let fileName = 'productos.xlsx';
  
        if (contentDisposition) {
          const matches = /filename="([^"]+)"/.exec(contentDisposition);
          if (matches?.length) fileName = matches[1];
        }
  
        a.download = fileName;
        a.click();
  
        window.URL.revokeObjectURL(url);
      },
      error: () => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo descargar el archivo',
          life: 3000
        });
      }
    });
  }
  
}