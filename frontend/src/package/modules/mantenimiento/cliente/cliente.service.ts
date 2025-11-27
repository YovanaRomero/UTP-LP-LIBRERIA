import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cliente, ClienteCreate, ClienteUpdate } from './cliente.model';
import { environment } from "src/environments/environment";

@Injectable({
    providedIn: 'root'
})
export class ClienteService {
    private apiUrl = environment.services.SisCore  + 'clientes';

    constructor(private http: HttpClient) {}

    getAll(): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(this.apiUrl);
    }

    getById(id: number): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.apiUrl}/${id}`);
    }

    create(cliente: ClienteCreate): Observable<Cliente> {
    return this.http.post<Cliente>(this.apiUrl, cliente);
    }

    update(id: number, cliente: ClienteUpdate): Observable<Cliente> {
    return this.http.put<Cliente>(`${this.apiUrl}/${id}`, cliente);
    }

    delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
    }

    search(termino: string): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.apiUrl}/search?q=${termino}`);
    }
}
