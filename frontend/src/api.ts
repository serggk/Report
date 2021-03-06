import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileUpdate, IUserProfileCreate, IReportRecord, IOpcoRecord, IOpcoRecordCreate } from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getReport(date: Date, token: string) {
    const headers = authHeaders(token);
    const params = {
      headers: headers.headers,
      params: {dt: date.toISOString().substr(0, 10)},
    };
    return axios.get<IReportRecord[]>(`${apiUrl}/api/report/`, params);
  },
  async uploadReport(formData: FormData, token: string) {
    return axios.post(`${apiUrl}/api/report/uploadfile`, formData, authHeaders(token));
  },
  async getOpco(token: string) {
    return axios.get<IOpcoRecord[]>(`${apiUrl}/api/opco/`, authHeaders(token));
  },
  async createOpco(token: string, data: IOpcoRecordCreate) {
    return axios.post<IOpcoRecord>(`${apiUrl}/api/opco/`, data, authHeaders(token));
  },
  async updateOpco(token: string, opcoId: number, data: IOpcoRecordCreate) {
    return axios.put<IOpcoRecord>(`${apiUrl}/api/opco/${opcoId}`, data, authHeaders(token));
  },
  async deleteOpco(token: string, opcoId: number) {
    return axios.delete<IOpcoRecord>(`${apiUrl}/api/opco/${opcoId}`, authHeaders(token));
  },
};
