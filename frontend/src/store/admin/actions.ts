import { api } from '@/api';
import { ActionContext } from 'vuex';
import { IUserProfileCreate, IUserProfileUpdate, IOpcoRecordCreate, IOpcoRecord } from '@/interfaces';
import { State } from '../state';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitSetUsers, commitSetUser, commitSetOpcos, commitSetOpco, commitDeleteOpco } from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from '../main/mutations';
import { AxiosError } from 'axios';

type MainContext = ActionContext<AdminState, State>;

export const actions = {
    async actionGetUsers(context: MainContext) {
        try {
            const response = await api.getUsers(context.rootState.main.token);
            if (response) {
                commitSetUsers(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionUpdateUser(context: MainContext, payload: { id: number, user: IUserProfileUpdate }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateUser(context.rootState.main.token, payload.id, payload.user),
                await new Promise((resolve, reject) => setTimeout(() => resolve(true), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateUser(context: MainContext, payload: IUserProfileCreate) {
        const loadingNotification = { content: 'saving', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createUser(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(true), 500)),
            ]))[0];
            commitSetUser(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: (error as AxiosError).response!.data.detail, color: 'error' });
            throw error;
        }
    },
    async actionGetOpco(context: MainContext) {
        try {
            const response = await api.getOpco(context.rootState.main.token);
            if (response) {
                commitSetOpcos(context, response.data);
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionCreateOpco(context: MainContext, payload: IOpcoRecordCreate) {
        const loadingNotification = { content: 'saving', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createOpco(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(true), 500)),
            ]))[0];
            commitSetOpco(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Company successfully created', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: (error as AxiosError).response!.data.detail, color: 'error' });
            throw error;
        }
    },
    async actionDeleteOpco(context: MainContext, payload: number) {
        const loadingNotification = { content: 'deleting', showProgress: true };
        try {
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.deleteOpco(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(true), 500)),
            ]))[0];
            commitDeleteOpco(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Company successfully deleted', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: (error as AxiosError).response!.data.detail, color: 'error' });
            throw error;
        }
    },
    async actionUpdateOpco(context: MainContext, payload: { id: number, opco: IOpcoRecord }) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateOpco(context.rootState.main.token, payload.id, payload.opco),
                await new Promise((resolve, reject) => setTimeout(() => resolve(true), 500)),
            ]))[0];
            commitSetOpco(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'User successfully updated', color: 'success' });
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const { dispatch } = getStoreAccessors<AdminState, State>('');

export const dispatchCreateUser = dispatch(actions.actionCreateUser);
export const dispatchGetUsers = dispatch(actions.actionGetUsers);
export const dispatchUpdateUser = dispatch(actions.actionUpdateUser);
export const dispatchGetOpco = dispatch(actions.actionGetOpco);
export const dispatchCreateOpco = dispatch(actions.actionCreateOpco);
export const dispatchUpdateOpco = dispatch(actions.actionUpdateOpco);
export const dispatchDeleteOpco = dispatch(actions.actionDeleteOpco);
