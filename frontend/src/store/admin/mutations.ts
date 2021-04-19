import { IOpcoRecord, IUserProfile } from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    setUsers(state: AdminState, payload: IUserProfile[]) {
        state.users = payload;
    },
    setUser(state: AdminState, payload: IUserProfile) {
        const users = state.users.filter((user: IUserProfile) => user.id !== payload.id);
        users.push(payload);
        state.users = users;
    },
    setOpcos(state: AdminState, payload: IOpcoRecord[]) {
        state.opco = payload;
    },
    setOpco(state: AdminState, payload: IOpcoRecord) {
        const opcos = state.opco.filter((company: IOpcoRecord) => company.id !== payload.id);
        opcos.push(payload);
        state.opco = opcos;
    },
    deleteOpco(state: AdminState, payload: IOpcoRecord) {
        const opco = state.opco.filter((company: IOpcoRecord) => company.id !== payload.id);
        state.opco = opco;
    },
};

const { commit } = getStoreAccessors<AdminState, State>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
export const commitSetOpcos = commit(mutations.setOpcos);
export const commitSetOpco = commit(mutations.setOpco);
export const commitDeleteOpco = commit(mutations.deleteOpco);
