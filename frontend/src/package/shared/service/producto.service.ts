import { Injectable } from "@angular/core";
import { environment } from "src/environments/environment";
import { Observable } from "rxjs";
import { HttpClient,HttpResponse  } from '@angular/common/http';
//Models
import { ProductoModel } from "@/shared/models/producto.model";

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
    //	Se hace una petición GET al endpoint del backend, permite acceder a los headers de la respuesta
    //el cual 'blob' indica un archivo binario
    //observe: 'response' permite acceder a los header de la respuesta, en ese caso al nombre del archivo.
    exportarExcel(): Observable<HttpResponse<Blob>> {
        const url = `${this.baseUrl}/exportar/excel`;

        return this.http.get(url, {
            responseType: 'blob',
            observe: 'response'
        });
    }
    
}
