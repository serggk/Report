import 'material-design-icons-iconfont/dist/material-design-icons.css';
import Vue from 'vue';
import Vuetify from 'vuetify';
import colors from 'vuetify/lib/util/colors';

Vue.use(Vuetify);

const opts = {
  theme: {
    themes: {
      light: {
        primary: colors.amber,
        secondary: colors.orange,
      },
    },
  },
};

export default new Vuetify(opts);
