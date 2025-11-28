import { Routes } from '@angular/router';

export default [
  {
    path: 'categoria',
    loadComponent: () =>
      import('./categoria/categoria.component').then(c => c.CategoriaComponent),
    data: { breadcrumb: 'Categorías' }
  },
  {
    path: 'producto',
    loadComponent: () =>
      import('./producto/producto.component').then(c => c.ProductoComponent),
    data: { breadcrumb: 'Productos' }
  },
  {
    path: 'cliente',
    loadComponent: () =>
      import('./cliente/cliente.component').then(c => c.ClienteComponent),
    data: { breadcrumb: 'Clientes' }
  }
] as Routes;