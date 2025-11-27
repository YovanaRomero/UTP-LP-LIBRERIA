import { HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs";

export declare interface IBaseService<T> {
    ListarPaginado(nPageNumber: number, nPageSize: number, sSortColumnName: string, sSortOrder: string, sFilterValue: string | null): void;
    Crear(oRequestModel: T): void;
    Actualizar(oRequestModel: T): void;
    Eliminar(sId: string | undefined): void;
    Exportar(extension: string, sId: string): Observable<HttpResponse<Blob>>;
}
