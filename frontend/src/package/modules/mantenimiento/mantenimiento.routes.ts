import { Routes } from '@angular/router';

export default [
    {
        path: 'categoria',
        loadComponent: () => import('./categoria/categoria').then((c) => c.Categoria),
        data: { breadcrumb: 'Categorias' }
    },
    {
        path: 'producto',
        loadComponent: () => import('./producto/producto').then((c) => c.Producto),
        data: { breadcrumb: 'Productos' }
    },
    {
        path: 'cliente',
        loadComponent: () => import('./cliente/cliente').then((c) => c.Cliente),
        data: { breadcrumb: 'Clientes' }
    },
] as Routes;
