import { ReportState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    reportRecords: (state: ReportState) => state.records,
    reportDate: (state: ReportState) => state.date,
};

const { read } = getStoreAccessors<ReportState, State>('');

export const readReportRecords = read(getters.reportRecords);
export const readReportDate = read(getters.reportDate);
