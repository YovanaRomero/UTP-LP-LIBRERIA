import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
    providedIn: 'root'
})
export class LoggerService {
    private readonly LOGSEQ_API_URL = 'https://www.google.com:80'; // Puerto predeterminado de Logseq

    constructor(private oHttpClient: HttpClient) {}

    public logDebug(method: string, data: any) {
        if (environment.enableBaseServiceLogs) {
            console.info(`${method}:`, data);
        }
    }
    public logError(method: string, data: any) {
        if (environment.enableBaseServiceLogs) {
            console.error(`${method}:`, data);
        }
    }

    logSeq(error: any) {
        const errorData = {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            userAgent: navigator.userAgent,
            error: {
                message: error.message,
                stack: error.stack,
                name: error.name
            }
        };

        return this.oHttpClient.post(this.LOGSEQ_API_URL, errorData);
    }
}
