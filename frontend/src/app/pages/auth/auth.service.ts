import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { SweetAltert2Service } from '@/services/sweetaltert2.service';
import { environment } from 'src/environments/environment';
import { firstValueFrom } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class AuthService {
    private http = inject(HttpClient);
    private router = inject(Router);
    private alert = inject(SweetAltert2Service);

    /**
     * Intenta iniciar sesión contra el endpoint de usuarios.
     * - Navega a `/` si la respuesta tiene `access_token`.
     * - Muestra alertas en caso de error.
     */
    async login(username: string, password: string) {
        const url = environment.services.SisCore + 'usuarios/login';
        try {
            const res: any = await firstValueFrom(
                this.http.post(url, { usuario_nombre: username, usuario_password: password })
            );

            if (res && res.access_token) {
                localStorage.setItem('access_token', res.access_token);
                if (res.usuario_nombre) localStorage.setItem('usuario_nombre', res.usuario_nombre);
                if (res.usuario_descripcion) localStorage.setItem('usuario_descripcion', res.usuario_descripcion);
                this.alert.success('Bienvenido', 'Inicio de sesión correcto');
                await this.router.navigate(['/']);
                return res;
            } else {
                this.alert.error('Error', 'Respuesta inválida del servidor');
                return null;
            }
        } catch (error: any) {
            const message = error?.error?.detail || error?.message || 'Error al iniciar sesión';
            this.alert.error('Error', message);
            return null;
        }
    }

    logout(){
        localStorage.removeItem('usuario_nombre');
        localStorage.removeItem('usuario_descripcion');
        localStorage.removeItem('access_token');
        this.router.navigate(['/auth/login']);
    }
}
