export interface IPagedResponseDto<T> {
    PageNumber: number;
    PageSize: number;
    TotalNumberOfPages: number;
    TotalNumberOfRecords: number;
    Results: T[];
}

export class PagedResponseModel<T> implements IPagedResponseDto<T> {
    constructor() {
        this.PageNumber = 0;
        this.PageSize = 0;
        this.TotalNumberOfPages = 0;
        this.TotalNumberOfRecords = 0;
        this.Results = [];
    }
    PageNumber: number = 0;
    PageSize: number = 0;
    TotalNumberOfPages: number = 0;
    TotalNumberOfRecords: number = 0;
    Results: T[] = [];
}

export interface IResponseModelDto<T> {
    bSuccess: boolean;
    sMessage: string;
    oData: any;
}

export interface IResponsePagedModelDto<T> {
    bSuccess: boolean;
    sMessage: string;
    oData: IPagedResponseDto<T>;
}


