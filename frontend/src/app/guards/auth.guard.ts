import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot } from "@angular/router";
import { AuthenticationService } from "../services/security/authentication.service";
import { LoggerService } from "../services/logger.service";

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
    constructor(
        private oLoggerService: LoggerService,
        private oAuthenticationService: AuthenticationService,
    ) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
        if (this.oAuthenticationService.isAuthenticated()) {
            this.oLoggerService.logDebug('AuthGuard - canActivate - isAuthenticated', true);
            return true;
        } else {
            this.oLoggerService.logDebug('AuthGuard - canActivate - isAuthenticated', false);
            localStorage.clear();
            //this.oAuthenticationService.goToLogin();
            this.oAuthenticationService.goToPreview();
            return false;
        }
    }
}
