import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { ReportState } from './state';

const defaultState: ReportState = {
  records: [],
  date: getCurrentDate(),
};

function getCurrentDate() {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d;
}

export const reportModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
