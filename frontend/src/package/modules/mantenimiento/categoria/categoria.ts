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
import { Table, TableLazyLoadEvent, TableModule } from 'primeng/table';
import { TextareaModule } from 'primeng/textarea';
import { ToastModule } from 'primeng/toast';
import { ToggleSwitchModule } from 'primeng/toggleswitch';
import { MessageModule } from 'primeng/message';
//Models
import { CategoriaModel } from '@/shared/models/categoria.model';

//Services
import { CategoriaService } from '@/shared/service/categoria.service';


@Component({
    selector: 'app-categoria',
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
    templateUrl: './categoria.html',
    styleUrl: './categoria.scss'
})
export class Categoria implements OnInit {

    @ViewChild('dt') dt!: Table;

    isLoading: boolean = true;
    categorias: CategoriaModel[] = [];
    categoriaDialog: boolean = false;
    categoria: CategoriaModel = {} as CategoriaModel;
    selectedCategorias: CategoriaModel[] = [];
    submitted: boolean = false;
    isEditMode: boolean = false;
    loading: boolean = false;

    estados = [
        { label: 'Activo', value: 1 },
        { label: 'Inactivo', value: 0 }
    ];

    constructor(
        private categoriaService: CategoriaService,
        private messageService: MessageService,
        private confirmationService: ConfirmationService
    ) {}

    ngOnInit(): void {
        this.loadCategorias();
    }


    loadCategorias(): void {
        this.loading = true;
        this.categoriaService.getAll().subscribe({
            next: (data) => {
            this.categorias = data;
            this.loading = false;
            },
            error: (err) => {
            this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudieron cargar las categorias',
                life: 3000
            });
            this.loading = false;
            }
        });
    }

    getChip(estado: number): string {
        switch (estado) {
            case 0:
                return 'chip-inactivo';
            case 1:
                return 'chip-activo';
            default:
                return 'chip-default';
        }
    }

    openNew(): void {
        this.categoria = {} as CategoriaModel;
        this.categoria.categoria_estado = 1; // Estado por defecto Activo
        this.submitted = false;
        this.isEditMode = false;
        this.categoriaDialog = true;
    }

    editCategoria(categoria: CategoriaModel): void {
        this.categoria = { ...categoria };
        this.isEditMode = true;
        this.categoriaDialog = true;
    }

    hideDialog(): void {
        this.categoriaDialog = false;
        this.submitted = false;
    }

    deleteCategoria(categoria: CategoriaModel): void {

      this.confirmationService.confirm({
      message: `¿Está seguro de eliminar la categoria ${categoria.categoria_nombre}?`,
      header: 'Confirmar',
      icon: 'pi pi-exclamation-triangle',
      accept: () => {
        if (categoria.categoria_id) {
          this.categoriaService.delete(categoria.categoria_id).subscribe({
            next: () => {
              this.categorias = this.categorias.filter(c => c.categoria_id !== categoria.categoria_id);
              this.messageService.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Categoria eliminada correctamente',
                life: 3000
              });
            },
            error: () => {
              this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudo eliminar el categoria',
                life: 3000
              });
            }
          });
        }
      }
    });

    }

    saveCategoria(): void {
        this.submitted = true;

        if (this.categoria.categoria_nombre?.trim() && this.categoria.categoria_descripcion?.trim()) {
        if (this.isEditMode && this.categoria.categoria_id) {
            this.categoriaService.update(this.categoria.categoria_id, this.categoria).subscribe({
            next: (data) => {
                const index = this.categorias.findIndex(c => c.categoria_id === data.categoria_id);
                if (index !== -1) {
                this.categorias[index] = data;
                }
                this.messageService.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Categoria actualizado correctamente',
                life: 3000
                });
                this.categoriaDialog = false;
                this.categoria = {} as CategoriaModel;
            },
            error: () => {
                this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudo actualizar la categoria',
                life: 3000
                });
            }
            });
        } else {
            this.categoriaService.create(this.categoria).subscribe({
            next: (data) => {
                this.categorias.push(data);
                this.messageService.add({
                severity: 'success',
                summary: 'Éxito',
                detail: 'Categoria creado correctamente',
                life: 3000
                });
                this.categoriaDialog = false;
                this.categoria = {} as CategoriaModel;
            },
            error: () => {
                this.messageService.add({
                severity: 'error',
                summary: 'Error',
                detail: 'No se pudo crear la categoria',
                life: 3000
                });
            }
            });
        }
        }
    }
}
