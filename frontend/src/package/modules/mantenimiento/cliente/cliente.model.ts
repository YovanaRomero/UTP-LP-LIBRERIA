export interface Cliente {
  cliente_id?: number;
  cliente_guid?: string;
  cliente_dni: string;
  cleinte_nombres: string;
  cliente_apellidos: string;
  cliente_direccion?: string;
  cliente_distrito?: string;
  cliente_correo?: string;
  cliente_celular?: string;
  cliente_estado?: number;
}

export interface ClienteCreate {
  cliente_dni: string;
  cleinte_nombres: string;
  cliente_apellidos: string;
  cliente_direccion?: string;
  cliente_distrito?: string;
  cliente_correo?: string;
  cliente_celular?: string;
  cliente_estado?: number;
}

export interface ClienteUpdate {
  cliente_dni?: string;
  cleinte_nombres?: string;
  cliente_apellidos?: string;
  cliente_direccion?: string;
  cliente_distrito?: string;
  cliente_correo?: string;
  cliente_celular?: string;
  cliente_estado?: number;
}
