import { Component, computed } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { DrawerModule } from 'primeng/drawer';
import { BadgeModule } from 'primeng/badge';
import { LayoutService } from '@/layout/service/layout.service';

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
                    >Romero Gutierrez Yovana</span
                >

                <ul class="list-none m-0 p-0">
                    <li>
                        <a class="cursor-pointer flex mb-4 p-4 items-center border border-surface-200 dark:border-surface-700 rounded hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors duration-150" >
                            <span>
                                <i class="pi pi-user text-xl text-primary"></i>
                            </span>
                            <div class="ml-4">
                                <span class="mb-2 font-semibold">Usuario</span>
                                <p class="text-surface-500 dark:text-surface-400 m-0">Login: Romero Gutierrez Yovana</p>
                                <p class="text-surface-500 dark:text-surface-400 m-0">Rol Actual: FullStack</p>
                            </div>
                        </a>
                    </li>
                    <li>
                        <a class="cursor-pointer flex mb-4 p-4 items-center border border-surface-200 dark:border-surface-700 rounded hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors duration-150">
                            <span>
                                <i class="pi pi-power-off text-xl text-primary"></i>
                            </span>
                            <div class="ml-4">
                                <span class="mb-2 font-semibold">Cerrar Sesión</span>
                                <p class="text-surface-500 dark:text-surface-400 m-0">
                                    13/11/2024 - 10:30 AM
                                </p>
                            </div>
                        </a>
                    </li>
                </ul>
            </div>
        </p-drawer>
    `,
})
export class AppProfileSidebar {
    constructor(public layoutService: LayoutService) {}

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
