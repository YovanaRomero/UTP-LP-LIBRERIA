import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { DrawerModule } from 'primeng/drawer';
import { BadgeModule } from 'primeng/badge';
import { LayoutService } from '@/layout/service/layout.service';
import { AuthService } from '@/pages/auth/auth.service';

@Component({
    selector: '[app-profilesidebar]',
    imports: [
        ButtonModule,
        DrawerModule,
        BadgeModule,
    ],
    template: `
        <p-drawer
            [visible]="visible()"
            (onHide)="onDrawerHide()"
            position="right"
            [transitionOptions]="'.3s cubic-bezier(0, 0, 0.2, 1)'"
            styleClass="layout-profile-sidebar w-full sm:w-25rem"
        >
            <div class="flex flex-col mx-auto md:mx-0">
                <span class="mb-2 font-semibold">Welcome</span>
                <span
                    class="text-surface-500 dark:text-surface-400 font-medium mb-8"
                    >{{usuarioName()}}</span
                >

                <ul class="list-none m-0 p-0">
                    <li>
                        <a class="cursor-pointer flex mb-4 p-4 items-center border border-surface-200 dark:border-surface-700 rounded hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors duration-150" >
                            <span>
                                <i class="pi pi-user text-xl text-primary"></i>
                            </span>
                            <div class="ml-4">
                                <span class="mb-2 font-semibold">Usuario</span>
                                <p class="text-surface-500 dark:text-surface-400 m-0">Login: {{ usuarioLogeado()}}</p>
                                <p class="text-surface-500 dark:text-surface-400 m-0">Rol Actual: FullStack</p>
                            </div>
                        </a>
                    </li>
                    <li>
                        <button (click)="authService.logout()" class="cursor-pointer flex mb-4 p-4 items-center border border-surface-200 dark:border-surface-700 rounded hover:bg-red-600  dark:hover:bg-surface-800 transition-colors duration-150 group">
                            <span>
                                <i class="pi pi-power-off text-xl text-primary group-hover:text-white"></i>
                            </span>
                            <div class="ml-4">
                                <span class="mb-2 font-semibold group-hover:text-white">Cerrar Sesión</span>
                                <p class="text-surface-500 dark:text-surface-400 m-0 group-hover:text-white">
                                    13/11/2024 - 10:30 AM
                                </p>
                            </div>
                        </button>
                    </li>
                </ul>
            </div>
        </p-drawer>
    `,
})
export class AppProfileSidebar implements OnInit {
    authService = inject(AuthService)

    usuarioLogeado = signal("")
    usuarioName = signal("")

    constructor(public layoutService: LayoutService) {}

    ngOnInit(): void {
        this.usuarioLogeado.set(localStorage.getItem("usuario_nombre") ?? "usuario")
        this.usuarioName.set(localStorage.getItem("usuario_descripcion") ?? "Romero Gutierrez Yovana")
    }



    visible = computed(
        () => this.layoutService.layoutState().profileSidebarVisible,
    );

    onDrawerHide() {
        this.layoutService.layoutState.update((state) => ({
            ...state,
            profileSidebarVisible: false,
        }));
    }
}
