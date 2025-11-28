import { Routes } from '@angular/router';

const MODULES_ROUTES: Routes = [
  {
    path: 'proceso',
    loadChildren: () =>
      import('./proceso/proceso.routes').then(m => m.default)
  },
  {
    path: 'mantenimiento',
    loadChildren: () =>
      import('./mantenimiento/mantenimiento.routes').then(m => m.default)
  }
];

export default MODULES_ROUTES;