import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { SweetAltert2Service } from '@/services/sweetaltert2.service';
import { environment } from 'src/environments/environment';
import { firstValueFrom } from 'rxjs';

import { PunkuSesionModel } from 'src/app/models/punku.model';
import { LoggerService } from '../../services/logger.service';
import { StorageService } from '../../services/security/storage.service';

@Injectable({
    providedIn: 'root',
})
export class AuthService {

    private userSession!: PunkuSesionModel;

    private http = inject(HttpClient);
    private router = inject(Router);
    private alert = inject(SweetAltert2Service);
    private oLoggerService = inject(LoggerService);
    private oStorageService= inject(StorageService);

    async login(username: string, password: string) {
        const url = environment.services.SisCore + 'usuarios/login';

        try {
            const res: any = await firstValueFrom(
                this.http.post(url, { usuario_nombre: username, usuario_password: password })
            );

            if (res && res.access_token) {
                const tokenJWT = res.access_token;
                // Guardar el token en el almacenamiento
                this.oLoggerService.logDebug('authentication.Service.ts - PunkuGetTokenUrl', tokenJWT);
                this.oStorageService.setItem('JWT',tokenJWT);

                this.userSession = JSON.parse(JSON.stringify(res));
                this.oLoggerService.logDebug('authentication.Service.ts - SesionAllData', this.userSession);
                this.oStorageService.setItem('SSO',JSON.stringify(this.userSession));
                this.router.navigate(['/']);
                return res;
            } else {
                this.oLoggerService.logError('authentication.Service.ts - PunkuGetTokenUrl', 'Error al iniciar sesión: access_token no encontrado');
                return null;
            }
        } catch (error: any) {
            const message = error?.error?.detail || error?.message || 'Error al iniciar sesión';
            this.alert.error('Error', error?.error?.detail);
            return null;
        }
    }

    logout(){
        localStorage.clear();
        this.oStorageService.removeItem('JWT');
        this.oStorageService.removeAll();
        this.oStorageService.removeItem('SSO');
        this.oLoggerService.logDebug('AuthenticationService - goToLogin','Redireccionando a PUNKU v2.0.0');
        window.location.href = 'http://localhost:4200/auth/login';
    }
}
