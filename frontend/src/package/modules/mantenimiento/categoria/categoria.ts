import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { IResponseModelDto, IResponsePagedModelDto, PagedResponseModel } from '@/models/response.model';
/*import { CargoService } from '@/shared/services/cargo.service';
import { TipoProcesoService } from '@/shared/services/tipo-proceso.service';
import { SharedModule } from '@/shared/shared.module';
import { fnFormatStringOrArrayOrUndefinedToString, fnValidateStringOrArrayOrUndefinedLong } from '@/shared/utils/string.util';
*/
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
//import { MessageService } from 'primeng/api';
import { BlockUI } from 'primeng/blockui';
import { ButtonModule } from 'primeng/button';
import { Chip, ChipModule } from 'primeng/chip';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';
import { Table, TableLazyLoadEvent, TableModule } from 'primeng/table';
import { TextareaModule } from 'primeng/textarea';
import { ToastModule } from 'primeng/toast';
import { ToggleSwitchModule } from 'primeng/toggleswitch';

import { CategoriaModel } from '@/shared/models/categoria.model';

@Component({
    selector: 'app-categoria',
    imports: [
        BlockUI,
        ToastModule,
        TableModule,
        ChipModule,
        ButtonModule,
        //SharedModule,
        DialogModule,
        ReactiveFormsModule,
        CommonModule,
        InputTextModule,
        TextareaModule,
        ToggleSwitchModule

    ],
    templateUrl: './categoria.html',
    styleUrl: './categoria.scss'
})
export class Categoria {
    isLoading: boolean = true;

      cols: any[] = [];
  rowsPerPageOptions = [10, 25, 75, 100];
  selectedRows: CategoriaModel[] = [];

    pagedResponseModel: PagedResponseModel<CategoriaModel> =
    new PagedResponseModel<CategoriaModel>();




  fnOnLazyLoadMaster(event: TableLazyLoadEvent): void {
    /*
    if (fnValidateStringOrArrayOrUndefinedLong(event.globalFilter)) {
      this.paginatorPage =
        (event.first as number) / (event.rows as number) + 1;
      this.paginatorSize = event.rows as number;
      this.fnRefreshRowsMaster(
        this.paginatorPage,
        this.paginatorSize,
        fnFormatStringOrArrayOrUndefinedToString(event.globalFilter),
      );
    }*/
  }
  fnRefreshRowsMaster(paginatorPage: number, paginatorSize: number, filterValue: string | null): void {
    this.isLoading = true;
/*
    this.cargoService
      .ListarPaginado(
        paginatorPage,
        paginatorSize,
        '',
        '',
        ''
      )
      .then((response: IResponsePagedModelDto<CategoriaModel>) => {
        if (response.bSuccess) {
          this.pagedResponseModel = response.oData;
        } else {
          this.pagedResponseModel = {
            Results: [],
            PageNumber: 1,
            PageSize: 10,
            TotalNumberOfRecords: 0,
            TotalNumberOfPages: 0
          };

          this.messageService.add({
            severity: 'warn',
            summary: 'Advertencia',
            detail: response.sMessage,
            life: 5000
          });
        }
      })
      .finally(() => {
        this.isLoading = false;
      });

      */
  }


}
