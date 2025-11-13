import { Routes } from '@angular/router';

export default [
    {
        path: 'proceso',
        loadChildren: () => import('./proceso/proceso.routes'),
        data: { breadcrumb: 'Proceso' }
    },
    {
        path: 'mantenimiento',
        loadChildren: () => import('./mantenimiento/mantenimiento.routes'),
        data: { breadcrumb: 'Mantenimiento' }
    }
] as Routes;
