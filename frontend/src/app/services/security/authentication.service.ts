import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { StorageService } from './storage.service';
import { environment } from 'src/environments/environment';
import { JwtHelperService } from '@auth0/angular-jwt';
import { HttpClient } from '@angular/common/http';
import { PunkuSesionModel } from 'src/app/models/punku.model';
import { LoggerService } from '../logger.service';
@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
    // Add this property to the class
    jwtHelper: JwtHelperService = new JwtHelperService();
    private userSubject: BehaviorSubject<PunkuSesionModel>;
    public user: Observable<PunkuSesionModel>;
    private userSession!: PunkuSesionModel;

    constructor(
        private oLoggerService: LoggerService,
        private oStorageService: StorageService,
        private activatedRoute: ActivatedRoute,
        private router: Router,
        private oHttpClient: HttpClient) {

        this.userSubject = new BehaviorSubject<PunkuSesionModel>(JSON.parse(this.oStorageService.getItem('SSO')));
        this.user = this.userSubject.asObservable();
    }

    public get userValue(): PunkuSesionModel {
        return this.userSubject.value;
    }

    logout() {
        localStorage.clear();
        this.oStorageService.removeItem('JWT');
        //this.userSubject.next(null);
        this.oStorageService.removeAll();
        this.clearDataInformationPublicLocal();
        this.goToLogin();
    }

    saveDataInformationPublicLocal(input: PunkuSesionModel) {
        this.oStorageService.setItem('SSO', JSON.stringify(input));
    }

    getDataInformationPublicLocal(): PunkuSesionModel {
        return JSON.parse(this.oStorageService.getItem('SSO'));
    }

    clearDataInformationPublicLocal() {
        this.oStorageService.removeItem('SSO');
    }

    isAuthenticated(): boolean {
        //Verificar si la URL comienza con '/auth/login'
        if (this.activatedRoute.snapshot.url.toString().startsWith('/auth/login'))
            return true;
        //Obtener el token del almacenamiento
        let token = this.oStorageService.getItem('JWT');
        if (token === null)
            return false;
        // Verificar si el token existe y no ha expirado
        return this.jwtHelper.isTokenExpired(token) === false && this.isAuthenticatedInValue();
    }

    isAuthenticatedInValue(): boolean {
        // Implementa lógica adicional si es necesario para verificar otras condiciones de autenticación
        // por ejemplo, verifica roles, permisos, etc.
        const token = this.oStorageService.getItem('JWT');
        if (token == null) {
            return false;
        }
        const decodedToken = this.jwtHelper.decodeToken(token);
        if (decodedToken == null) {
            return false;
        }
        this.oLoggerService.logDebug('AuthenticationService - isAuthenticatedInValue',decodedToken);
        return true
        //return atob(decodedToken.Autenticado) === '1';
    }

    getUser(): PunkuSesionModel {
        let dataAuthentication = JSON.parse(this.oStorageService.getItem('SSO'));
        //if(!dataAuthentication)return null;
        return dataAuthentication;

    }
    goToPreview(){
        this.router.navigate(['/home']);
    }
    goToLogin(){
        this.oLoggerService.logDebug('AuthenticationService - goToLogin','Redireccionando a PUNKU v2.0.0');
        window.location.href = 'http://localhost:4200/auth/login'; //environment.PunkuApiv2.PunkuLoginUrl.replace('{0}',btoa(JSON.stringify(param)));
    }

    getTokenByCodeAndChallenge(code: string, challenge: string): void {
        /*const requestBody = {
            CODE: code,
            CODE_CHALLENGE: challenge
        };
        this.oHttpClient.post<any>(environment.PunkuApiv2.PunkuGetTokenUrl, requestBody)
            .subscribe(
                (response: any) => {
                    if (response.HasErrors === false) {
                        const tokenJWT = response.TOKEN_JWT;
                        //const guid_sistema = response.GUID_SISTEMA;
                        //console.log('GUID_SISTEMA:::', guid_sistema);
                        // Guardar el token en el almacenamiento
                        this.oLoggerService.logDebug('authentication.Service.ts - PunkuGetTokenUrl', tokenJWT);
                        this.oStorageService.setItem('JWT',tokenJWT);
                        //this.oStorageService.setItem('GUID_SISTEMA',guid_sistema);

                        //- Obtener los datos del usuario
                        this.oHttpClient.post<any>(environment.PunkuApiv2.PunkuSesionAllData, requestBody)
                        .subscribe(
                            (response: any) => {
                                if (response.HasErrors === false) {
                                    this.userSession = JSON.parse(JSON.stringify(response));
                                    this.userSession.ROL_USUARIO.forEach(rol => {
                                        // Validar cual es el rol por defecto
                                        if (rol.POR_DEFECTO) {
                                            this.userSession.SESION.GUID_ROL = rol.GUID_ROL ?? '';
                                            this.userSession.SESION.NOMBRE_ROL = rol.NOMBRE_ROL ?? '';
                                            this.userSession.SESION.GUID_SEDE = rol.GUID_SEDE ?? '';
                                            this.userSession.SESION.DESCRIPCION_SEDE = rol.DESCRIPCION_SEDE ?? '';
                                        }
                                    });
                                    this.oLoggerService.logDebug('authentication.Service.ts - SesionAllData', this.userSession);
                                    this.oStorageService.setItem('SSO',JSON.stringify(this.userSession));
                                    //this.oStorageService.setItem('SESION',JSON.stringify(response.SESION));
                                    //this.oStorageService.setItem('USUARIO',JSON.stringify(response.USUARIO));
                                    //this.oStorageService.setItem('ROL_USUARIO',JSON.stringify(response.ROL_USUARIO));
                                    //this.oStorageService.setItem('MENU',JSON.stringify(response.MENU));
                                    this.router.navigate(['/']);

                                } else {
                                    this.oLoggerService.logError('authentication.Service.ts - SesionAllData', response.Messages);
                                }
                            },
                            (error) => {
                                this.oLoggerService.logError('authentication.Service.ts - SesionAllData', error);
                                // Aquí maneja el error, por ejemplo, redirigiendo a una página de error o mostrando un mensaje al usuario
                                this.router.navigate(['/notfound']);
                            }
                        );
                        //- Fin Obtener los datos del usuario
                    } else {
                        this.oLoggerService.logError('authentication.Service.ts - PunkuGetTokenUrl', response.Messages);
                    }
                },
                (error) => {
                    this.oLoggerService.logError('authentication.Service.ts - PunkuGetTokenUrl', error);
                    // Aquí maneja el error, por ejemplo, redirigiendo a una página de error o mostrando un mensaje al usuario
                    this.router.navigate(['/notfound']);
                }
            );
        */
    }
}
