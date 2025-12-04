import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { firstValueFrom } from "rxjs";

/**
 * Interfaz de Producto para el CRUD
 */
export interface Product {
    id?: string;
    code?: string;
    name?: string;
    description?: string;
    image?: string;
    price?: number;
    category?: string;
    rating?: number;
    inventoryStatus?: string;
    quantity?: number;
}

/**
 * Interfaz de respuesta del API
 */
export interface ApiResponse<T> {
    status?: number;
    message?: string;
    data?: T;
    timestamp?: string;
}

@Injectable({
    providedIn: 'root',
})
export class ProductService {
    private http = inject(HttpClient);
    private apiUrl = `${environment.services.SisCore}productos`;

    /**
     * Obtener todos los productos
     */
    async getProducts(): Promise<Product[]> {
        try {
            const response = await firstValueFrom(
                this.http.get<ApiResponse<Product[]>>(this.apiUrl)
            );
            return response.data || [];
        } catch (error) {
            console.error('Error al obtener productos:', error);
            return [];
        }
    }

    /**
     * Obtener un producto por ID
     */
    async getProduct(id: string): Promise<Product | null> {
        try {
            const response = await firstValueFrom(
                this.http.get<ApiResponse<Product>>(`${this.apiUrl}/${id}`)
            );
            return response.data || null;
        } catch (error) {
            console.error('Error al obtener producto:', error);
            return null;
        }
    }

    /**
     * Crear un nuevo producto
     */
    async createProduct(product: Product): Promise<Product | null> {
        try {
            const response = await firstValueFrom(
                this.http.post<ApiResponse<Product>>(this.apiUrl, product)
            );
            return response.data || null;
        } catch (error) {
            console.error('Error al crear producto:', error);
            return null;
        }
    }

    /**
     * Actualizar un producto
     */
    async updateProduct(id: string, product: Product): Promise<Product | null> {
        try {
            const response = await firstValueFrom(
                this.http.put<ApiResponse<Product>>(`${this.apiUrl}/${id}`, product)
            );
            return response.data || null;
        } catch (error) {
            console.error('Error al actualizar producto:', error);
            return null;
        }
    }

    /**
     * Eliminar un producto
     */
    async deleteProduct(id: string): Promise<boolean> {
        try {
            await firstValueFrom(
                this.http.delete<ApiResponse<void>>(`${this.apiUrl}/${id}`)
            );
            return true;
        } catch (error) {
            console.error('Error al eliminar producto:', error);
            return false;
        }
    }

    /**
     * Buscar productos por nombre
     */
    async searchProducts(query: string): Promise<Product[]> {
        try {
            const response = await firstValueFrom(
                this.http.get<ApiResponse<Product[]>>(`${this.apiUrl}/search`, {
                    params: { q: query }
                })
            );
            return response.data || [];
        } catch (error) {
            console.error('Error al buscar productos:', error);
            return [];
        }
    }

    /**
     * Obtener productos por categoría
     */
    async getProductsByCategory(category: string): Promise<Product[]> {
        try {
            const response = await firstValueFrom(
                this.http.get<ApiResponse<Product[]>>(`${this.apiUrl}/categoria/${category}`)
            );
            return response.data || [];
        } catch (error) {
            console.error('Error al obtener productos por categoría:', error);
            return [];
        }
    }
}
