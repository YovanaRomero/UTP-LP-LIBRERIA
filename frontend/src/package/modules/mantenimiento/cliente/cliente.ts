import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Table, TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { ToolbarModule } from 'primeng/toolbar';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ToastModule } from 'primeng/toast';
import { ConfirmationService, MessageService } from 'primeng/api';
import { ClienteService } from './cliente.service';
import { Cliente } from './cliente.model';

@Component({
  selector: 'app-cliente',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    TableModule,
    ButtonModule,
    DialogModule,
    InputTextModule,
    ToolbarModule,
    ConfirmDialogModule,
    ToastModule
  ],
  providers: [ConfirmationService, MessageService],
  templateUrl: './cliente.html',
  styleUrl: './cliente.scss',
})
export class ClienteComponent implements OnInit {
  @ViewChild('dt') dt!: Table;

  clientes: Cliente[] = [];
  clienteDialog: boolean = false;
  cliente: Cliente = {} as Cliente;
  selectedClientes: Cliente[] = [];
  submitted: boolean = false;
  isEditMode: boolean = false;
  loading: boolean = false;

  constructor(
    private clienteService: ClienteService,
    private messageService: MessageService,
    private confirmationService: ConfirmationService
  ) {}

  ngOnInit(): void {
    this.loadClientes();
  }

  loadClientes(): void {
    this.loading = true;
    this.clienteService.getAll().subscribe({
      next: (data) => {
        this.clientes = data;
        this.loading = false;
      },
      error: (err) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudieron cargar los clientes',
          life: 3000
        });
        this.loading = false;
      }
    });
  }

  openNew(): void {
    this.cliente = {} as Cliente;
    this.submitted = false;
    this.isEditMode = false;
    this.clienteDialog = true;
  }

  editCliente(cliente: Cliente): void {
    this.cliente = { ...cliente };
    this.isEditMode = true;
    this.clienteDialog = true;
  }

  deleteCliente(cliente: Cliente): void {
    this.confirmationService.confirm({
      message: `¿Está seguro de eliminar al cliente ${cliente.cliente_nombres} ${cliente.cliente_apellidos}?`,
      header: 'Confirmar',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        if (cliente.cliente_id) {
          this.clienteService.delete(cliente.cliente_id).subscribe({
            next: () => {
              this.clientes = this.clientes.filter(c => c.cliente_id !== cliente.cliente_id);
              this.messageService.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Cliente eliminado',
                life: 3000
              });
            },
            error: () => {
              this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudo eliminar el cliente',
                life: 3000
              });
            }
          });
        }
      }
    });
  }

  hideDialog(): void {
    this.clienteDialog = false;
    this.submitted = false;
  }

  saveCliente(): void {
    this.submitted = true;

    if (this.cliente.cliente_dni?.trim() && this.cliente.cliente_nombres?.trim()) {
      if (this.isEditMode && this.cliente.cliente_id) {
        this.clienteService.update(this.cliente.cliente_id, this.cliente).subscribe({
          next: (data) => {
            const index = this.clientes.findIndex(c => c.cliente_id === data.cliente_id);
            if (index !== -1) {
              this.clientes[index] = data;
            }
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: 'Cliente actualizado',
              life: 3000
            });
            this.clienteDialog = false;
            this.cliente = {} as Cliente;
          },
          error: () => {
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo actualizar el cliente',
              life: 3000
            });
          }
        });
      } else {
        this.clienteService.create(this.cliente).subscribe({
          next: (data) => {
            this.clientes.push(data);
            this.messageService.add({
              severity: 'success',
              summary: 'Éxito',
              detail: 'Cliente creado',
              life: 3000
            });
            this.clienteDialog = false;
            this.cliente = {} as Cliente;
          },
          error: () => {
            this.messageService.add({
              severity: 'error',
              summary: 'Error',
              detail: 'No se pudo crear el cliente',
              life: 3000
            });
          }
        });
      }
    }
  }

  onGlobalFilter(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.dt.filterGlobal(value, 'contains');
  }
}
