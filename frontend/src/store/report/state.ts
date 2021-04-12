import { IOpcoRecord, IReportRecord } from '@/interfaces';

export interface ReportState {
    records: IReportRecord[];
    date: Date;
}
