import { api } from '@/api';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { ReportState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetReportRecords, commitSetReportDate } from './mutations';
import { dispatchCheckApiError } from '../main/actions';

type MainContext = ActionContext<ReportState, State>;

export const actions = {
    async actionGetReportRecords(context: MainContext) {
        try {
            const response = await api.getReport(context.state.date, context.rootState.main.token);
            if (response) {
                commitSetReportRecords(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },

    async actionSetReportDate(context: MainContext, payload: Date) {
        try {
            commitSetReportDate(context, payload);
            await dispatchGetReportRecords(context);
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<ReportState, State>('');

export const dispatchGetReportRecords = dispatch(actions.actionGetReportRecords);
export const dispatchSetReportDate = dispatch(actions.actionSetReportDate);
