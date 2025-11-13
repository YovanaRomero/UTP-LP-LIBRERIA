import { Component, ElementRef, ViewChild } from '@angular/core';
import { AppMenu } from './app.menu';
import { LayoutService } from '@/layout/service/layout.service';
import { RouterModule } from '@angular/router';

@Component({
    selector: '[app-sidebar]',
    standalone: true,
    imports: [AppMenu, RouterModule],
    template: ` <div
        class="layout-sidebar"
        (mouseenter)="onMouseEnter()"
        (mouseleave)="onMouseLeave()"
    >
        <div class="sidebar-header">
            <a [routerLink]="['/']" class="app-logo">
                <svg xmlns="http://www.w3.org/2000/svg" height="85px" viewBox="0 0 250 250" version="1.1" alt="Logo Angular" class="icon">
                    <g>
                        <path d="M125,30L125,30L125,30L31.9,63.2l14.2,123.1L125,230l78.9-43.7l14.2-123.1L125,30z" fill="#DD0031"/>
                        <path d="M125,30L125,30L125,30L31.9,63.2l14.2,123.1L125,230l78.9-43.7l14.2-123.1L125,30z" fill="#DD0031"/>
                        <path d="M125,52.1L125,52.1L66.8,182.6h21.7l11.7-29.4h49.4l11.7,29.4h21.7L125,52.1z M142,135.4H108l17-40.9L142,135.4z" fill="#FFFFFF"/>
                    </g>
                </svg>
            </a>
            <button
                class="layout-sidebar-anchor p-link z-2 hover:cursor-pointer"
                type="button"
                (click)="anchor()"
            ></button>
        </div>

        <div #menuContainer class="layout-menu-container">
            <app-menu></app-menu>
        </div>
    </div>`,
})
export class AppSidebar {
    timeout: any = null;

    @ViewChild('menuContainer') menuContainer!: ElementRef;
    constructor(
        public layoutService: LayoutService,
        public el: ElementRef,
    ) {}

    onMouseEnter() {
        if (!this.layoutService.layoutState().anchored) {
            if (this.timeout) {
                clearTimeout(this.timeout);
                this.timeout = null;
            }

            this.layoutService.layoutState.update((state) => {
                if (!state.sidebarActive) {
                    return {
                        ...state,
                        sidebarActive: true,
                    };
                }
                return state;
            });
        }
    }

    onMouseLeave() {
        if (!this.layoutService.layoutState().anchored) {
            if (!this.timeout) {
                this.timeout = setTimeout(() => {
                    this.layoutService.layoutState.update((state) => {
                        if (state.sidebarActive) {
                            return {
                                ...state,
                                sidebarActive: false,
                            };
                        }
                        return state;
                    });
                }, 300);
            }
        }
    }

    anchor() {
        this.layoutService.layoutState.update((state) => ({
            ...state,
            anchored: !state.anchored,
        }));
    }
}
