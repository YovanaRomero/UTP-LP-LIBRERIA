import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AppMenuitem } from './app.menuitem';

@Component({
    selector: 'app-menu',
    standalone: true,
    imports: [CommonModule, AppMenuitem, RouterModule],
    template: `<ul class="layout-menu">
        <ng-container *ngFor="let item of model; let i = index">
            <li
                app-menuitem
                *ngIf="!item.separator"
                [item]="item"
                [index]="i"
                [root]="true"
            ></li>
            <li *ngIf="item.separator" class="menu-separator"></li>
        </ng-container>
    </ul> `,
})
export class AppMenu {
    model: any[] = [];

    ngOnInit() {
        this.model = [
            {
                label: 'Proceso',
                icon: 'pi pi-home',
                items: [
                    {
                        label: 'Pedidos',
                        icon: 'pi pi-fw pi-table',
                        routerLink: ['/modulos/proceso/pedido'],
                    }
                ],
            },
            {
                label: 'Mantenimiento',
                icon: 'pi pi-fw pi-star-fill',
                items: [
                    {
                        label: 'Categorias',
                        icon: 'pi pi-fw pi-list',
                        routerLink: ['/modulos/mantenimiento/categoria'],
                    },
                    {
                        label: 'Productos',
                        icon: 'pi pi-fw pi-check-square',
                        routerLink: ['/modulos/mantenimiento/producto'],
                    },
                    {
                        label: 'Clientes',
                        icon: 'pi pi-fw pi-id-card',
                        routerLink: ['/modulos/mantenimiento/cliente'],
                    }
                ],
            },
        ];
    }
}
