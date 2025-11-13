import { Routes } from '@angular/router';

export default [
    {
        path: 'pedido',
        loadComponent: () => import('./pedido/pedido').then((c) => c.Pedido),
        data: { breadcrumb: 'Proceso' }
    }
] as Routes;
