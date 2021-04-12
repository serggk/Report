import { IReportRecord } from '@/interfaces';
import { ReportState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setReportRecords(state: ReportState, payload: IReportRecord[]) {
        state.records = payload;
    },
    setReportDate(state: ReportState, payload: Date) {
        state.date = payload;
    },
};

const { commit } = getStoreAccessors<ReportState, State>('');

export const commitSetReportRecords = commit(mutations.setReportRecords);
export const commitSetReportDate = commit(mutations.setReportDate);
