import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, map, retry, throwError, timeout } from 'rxjs';
import { LoggerService } from './logger.service';
import { SweetAltert2Service } from '@/services/sweetaltert2.service';
@Injectable({
    providedIn: 'root',
})
export class BaseService {
    private TIMEOUT = 5000; // Timeout de 5 segundos
    constructor(
        private oLoggerService: LoggerService,
        private clienteHttp: HttpClient,
        private oSweetAltert2Service: SweetAltert2Service
    ) {}

    CallMockup(file: string): Observable<any> {
        return this.clienteHttp.get(`assets/demo/data/${file}`).pipe(
            retry(1),
            timeout(this.TIMEOUT),
            map(response => {
                this.oLoggerService.logDebug('BaseService - CallMockup', response);
                return response;
            }),
            catchError((err) => this.handleError(err))
        );
    }

    CallGet(metodo: string): Observable<any> {
        return this.clienteHttp.get(metodo).pipe(
            retry(1),
            timeout(this.TIMEOUT),
            map(response => {
                this.oLoggerService.logDebug('BaseService - CallGet', response);
                return response;
            }),
            catchError((err) => this.handleError(err))
        );
    }

    CallPost(metodo: string, request: any): Observable<any> {
        return this.clienteHttp.post(metodo, request).pipe(
            retry(1),
            timeout(this.TIMEOUT),
            map(response => {
                this.oLoggerService.logDebug('BaseService - CallPost', response);
                return response;
            }),
            catchError((err) => this.handleError(err))
        );
    }

    CallPut(metodo: string, request: any): Observable<any> {
        return this.clienteHttp.put(metodo, request).pipe(
            retry(1),
            timeout(this.TIMEOUT),
            map(response => {
                this.oLoggerService.logDebug('BaseService - CallPut', response);
                return response;
            }),
            catchError((err) => this.handleError(err))
        );
    }

    CallDelete(metodo: string): Observable<any> {
        return this.clienteHttp.delete(metodo).pipe(
            retry(1),
            timeout(this.TIMEOUT),
            map(response => {
                this.oLoggerService.logDebug('BaseService - CallDelete', response);
                return response;
            }),
            catchError((err) => this.handleError(err))
        );
    }

    // Error handling
    handleError(error: any) {
        const errorTime = new Date().toLocaleString();
        let errorMessage = '';
        if (error.error instanceof ErrorEvent) {
            // Get client-side error
            errorMessage = error.error.message;
        } else {
            // Get server-side error
            errorMessage = `Error Server Side: ${error.status}\nMessage: ${error.message}`;
        }
        this.oSweetAltert2Service.error('SUNEDU','El servidor no responde. Por favor, inténtalo más tarde.')
        return throwError(() => {
            console.error(`[${errorTime}] :`, errorMessage);
            return errorMessage; // Devuelve el mensaje de error para mostrarlo en la UI
        });
    }
}
