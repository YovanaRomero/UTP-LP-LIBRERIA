import { Routes } from '@angular/router';

export default [
  {
    path: 'pedido',
    loadComponent: () =>
      import('./pedido/pedido.component').then(m => m.PedidoComponent),
    data: { breadcrumb: 'Pedido' }
  }
] as Routes;
