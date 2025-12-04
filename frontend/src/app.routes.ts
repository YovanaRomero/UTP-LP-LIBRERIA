import { Routes } from '@angular/router';
import { AppLayout } from '@/layout/components/app.layout';
import { Landing } from '@/pages/landing/landing';
import { Notfound } from '@/pages/notfound/notfound';
import { AuthGuard } from './app/guards/auth.guard';
export const appRoutes: Routes = [
    {
        path: '',
        component: AppLayout,
        canActivate: [AuthGuard],
        children: [
            {
                path: 'pages',
                loadChildren: () => import('@/pages/pages.routes'),
            },
            {
                path: 'modulos',
                loadChildren: () => import('@/modules/modules.routes').then(m => m.default),
                data: { breadcrumb: 'Módulos' },
            }
        ],
    },
    //{ path: 'landing', component: Landing },
    { path: 'home', component: Landing },
    { path: 'notfound', component: Notfound },
    {
        path: 'auth',
        canActivate:[],
        loadChildren: () => import('@/pages/auth/auth.routes'),
    }
];
