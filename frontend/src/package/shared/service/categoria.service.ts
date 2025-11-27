import { Injectable } from "@angular/core";
import { IBaseService } from "@/shared/service/ibase.service";
import { environment } from "src/environments/environment";
import { HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";
import { HttpClient } from '@angular/common/http';
//Models
import { CategoriaModel } from "@/shared/models/categoria.model";
//Services
import { BaseService } from "@/shared/service/base.service";

@Injectable({
    providedIn: 'root'
})


export class CategoriaService {

    private baseUrl: string = environment.services.SisCore + 'categorias';

    constructor(private http: HttpClient) {}

    getAll(): Observable<CategoriaModel[]> {
        return this.http.get<CategoriaModel[]>(this.baseUrl);
    }

    getById(id: number): Observable<CategoriaModel> {
        return this.http.get<CategoriaModel>(`${this.baseUrl}/${id}`);
    }

    create(categoria: CategoriaModel): Observable<CategoriaModel> {
        return this.http.post<CategoriaModel>(this.baseUrl, categoria);
    }

    update(id: number, categoria: CategoriaModel): Observable<CategoriaModel> {
        return this.http.put<CategoriaModel>(`${this.baseUrl}/${id}`, categoria);
    }

    delete(id: number): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/${id}`);
    }

    search(termino: string): Observable<CategoriaModel[]> {
        return this.http.get<CategoriaModel[]>(`${this.baseUrl}/search?q=${termino}`);
    }
}
