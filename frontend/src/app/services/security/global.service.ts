import { Injectable } from '@angular/core';
import { StorageService } from './storage.service';

@Injectable({
    providedIn: 'root',
})
export class GlobalVariableService {
    constructor(private oStorageService: StorageService) {}

    public setTokem(value: any) {
        if (typeof value === 'string') {
            this.oStorageService.setItem('token', value);
        } else {
            this.oStorageService.setItem('token', JSON.stringify(value));
        }
    }

    public getTokem(): any {
        return JSON.parse(this.oStorageService.getItem('token'));
    }

    public setTokenJWT(token: string): void {
        this.oStorageService.setItem('JWT', token);
    }

    public removeItemLocalStorage(item: string): void {
        this.oStorageService.removeItem(item);
    }

    public removeItemComplete(): void {
        this.oStorageService.removeAll();
    }

    public getTokenJWT(): any {
        return this.oStorageService.getItem('JWT');
    }

    public setTokenCaptcha(token: string): void {
        this.oStorageService.setItem('Captcha', token);
    }

    public getTokenCaptcha(): any {
        return this.oStorageService.getItem('Captcha');
    }

    public setTokenAction(token: string): void {
        this.oStorageService.setItem('Token_Action', token);
    }

    public getTokenAction(): any {
        return this.oStorageService.getItem('Token_Action');
    }

    /* EXTENSION METHOD TO GET BROWSER COOKIE */
    public getCookie(cname: string): any {
        var name = cname + '=';
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return '';
    }

    /* convertDataURIToBinary */
    public convertDataURIToBinary(bytesFile: any) {
        var raw = window.atob(bytesFile);
        var rawLength = raw.length;
        var array = new Uint8Array(new ArrayBuffer(rawLength));

        for (var i = 0; i < rawLength; i++) {
            array[i] = raw.charCodeAt(i);
        }
        return array;
    }
}
