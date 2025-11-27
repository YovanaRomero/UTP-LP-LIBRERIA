import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { Observable } from "rxjs";
import { HttpClient } from '@angular/common/http';
//Models
import { ProductoModel } from "@/shared/models/producto.model";
//Services

@Injectable({
    providedIn: 'root'
})

export class ProductoService {

    private baseUrl: string = environment.services.SisCore + 'productos';

    constructor(private http: HttpClient) {}

    getAll(): Observable<ProductoModel[]> {
        return this.http.get<ProductoModel[]>(this.baseUrl);
    }

    getById(id: number): Observable<ProductoModel> {
        return this.http.get<ProductoModel>(`${this.baseUrl}/${id}`);
    }

    create(producto: ProductoModel): Observable<ProductoModel> {
        return this.http.post<ProductoModel>(this.baseUrl, producto);
    }

    update(id: number, producto: ProductoModel): Observable<ProductoModel> {
        return this.http.put<ProductoModel>(`${this.baseUrl}/${id}`, producto);
    }

    delete(id: number): Observable<void> {
        return this.http.delete<void>(`${this.baseUrl}/${id}`);
    }
}
