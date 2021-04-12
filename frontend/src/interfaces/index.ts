export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    opco?: IOpcoRecord;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    opco?: IOpcoRecord;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
    opco?: IOpcoRecord;
}

export interface IReportRecord {
    date: Date;
    time: Date;
    rx: number;
    tx: number;
    opco: string;
}

export interface IOpcoRecord {
    id: number;
    opco: string;
}
