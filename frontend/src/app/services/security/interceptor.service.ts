import { Injectable } from '@angular/core';
import {
    HttpEvent,
    HttpHandler,
    HttpInterceptor,
    HttpRequest,
} from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { StorageService } from './storage.service';
import { AuthenticationService } from './authentication.service';
import { environment } from 'src/environments/environment';
import { LoggerService } from '../logger.service';

@Injectable()
export class InterceptorService implements HttpInterceptor {
    // Lista de URLs que no requieren el encabezado de autorización
    private excludedUrls: string[] = [
        'http://localhost4200/auth/login',
    ];

    constructor(
        private oLoggerService: LoggerService,
        private oStorageService: StorageService,
        private oAuthenticationService: AuthenticationService
    ) {}

    intercept(
        request: HttpRequest<any>,
        next: HttpHandler
    ): Observable<HttpEvent<any>> {
        // Obtener el token de autenticación desde el almacenamiento local o las cookies
        this.oLoggerService.logDebug('Interceptando Request',request);
        const isExcludedUrl = this.excludedUrls.some((url) =>
            request.url.includes(url)
        );
        if (!isExcludedUrl) {
            let token = this.oStorageService.getItem('JWT');
            request = request.clone({
                setHeaders: {
                    Authorization: `Bearer ${token}`,
                },
            });
        }
        return next.handle(request).pipe(
            catchError((error) => {
                if (
                    error.status === 401 ||
                    !this.oAuthenticationService.isAuthenticated()
                ) {
                    this.oLoggerService.logDebug('Redireccionando a la página de login',null);
                    this.oAuthenticationService.logout();
                }
                this.oLoggerService.logError('Interceptando', error);
                return throwError(error);
            })
        );
    }
}
