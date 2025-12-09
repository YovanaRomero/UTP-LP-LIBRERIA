import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { PedidoRequest, PedidoModel } from '../models/pedido.model';
import { ClientePedidoModel } from '../models/cliente.model';

@Injectable({
  providedIn: 'root'
})
export class PedidoService {

  private apiUrl = environment.services.SisCore;

  constructor(private http: HttpClient) {}

  getPedidos(): Observable<PedidoModel[]> {
    return this.http.get<PedidoModel[]>(`${this.apiUrl}pedidos/`);
  }

  getPedido(id: number): Observable<PedidoModel> {
    return this.http.get<PedidoModel>(`${this.apiUrl}pedidos/${id}`);
  }

  createPedido(body: PedidoRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}pedidos/create`, body);
  }

  getClientes(): Observable<ClientePedidoModel[]> {
    return this.http.get<ClientePedidoModel[]>(`${this.apiUrl}clientes/`);
  }
}
