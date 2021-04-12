import { IOpcoRecord, IUserProfile } from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    opco: IOpcoRecord[];
}
