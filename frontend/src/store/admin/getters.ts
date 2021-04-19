import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    adminUsers: (state: AdminState) => state.users,
    adminOneUser: (state: AdminState) => (userId: number) => {
        const filteredUsers = state.users.filter((user) => user.id === userId);
        if (filteredUsers.length > 0) {
            return { ...filteredUsers[0] };
        }
    },
    adminOpco: (state: AdminState) => state.opco,
    adminOneOpco: (state: AdminState) => (opcoId: number) => {
        const filteredOpco = state.opco.filter((opco) => opco.id === opcoId);
        if (filteredOpco.length > 0) {
            return { ...filteredOpco[0] };
        }
    },
};

const { read } = getStoreAccessors<AdminState, State>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminUsers = read(getters.adminUsers);
export const readAdminOneOpco = read(getters.adminOneOpco);
export const readAdminOpco = read(getters.adminOpco);
