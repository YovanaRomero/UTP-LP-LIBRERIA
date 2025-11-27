import { Injectable } from "@angular/core";
import Swal from 'sweetalert2';
@Injectable({
    providedIn: 'root',
})
export class SweetAltert2Service {
    constructor() {}
    success(Title: string, Message: string) {
        Swal.fire({
            customClass: { container: 'swal2-container' },
            icon: 'success',
            title: Title,
            text: Message,
        });
    }
    error(Title: string, Message: string) {
        Swal.fire({
            customClass: { container: 'swal2-container' },
            icon: 'error',
            title: Title,
            text: Message,
        });
    }
    warning(Title: string, Message: string) {
        Swal.fire({
            customClass: { container: 'swal2-container' },
            icon: 'warning',
            title: Title,
            text: Message,
        });
    }
    confirm(Title: string, Message: string) {
        return Swal.fire({
            title: Title,
            text: Message,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            cancelButtonText: 'No',
            confirmButtonText: 'Si',
        });
    }
}
