import { Routes } from '@angular/router';
import { AppLayout } from '@/layout/components/app.layout';
import { Landing } from '@/pages/landing/landing';
import { Notfound } from '@/pages/notfound/notfound';

export const appRoutes: Routes = [
    {
        path: '',
        component: AppLayout,
        children: [
            {
                path: 'pages',
                loadChildren: () => import('@/pages/pages.routes'),
            },
            {
                path: 'modulos',
                loadChildren: () => import('@/modules/modules.routes'),
                data: { breadcrumb: 'Módulos' },
            }
        ],
    },
    { path: 'landing', component: Landing },
    { path: 'notfound', component: Notfound },
    {
        path: 'auth',
        loadChildren: () => import('@/pages/auth/auth.routes'),
    }
];
