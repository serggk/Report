<template>
  <div>
    <v-app-bar light>
      <v-app-bar-title> Report for user </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-menu
        v-model="menu2"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="date"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-text-field>
        </template>
        <v-date-picker v-model="date" @input="menu2 = false"></v-date-picker>
      </v-menu>
    </v-app-bar>
    <v-data-table :headers="headers" :items="records"> </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readHasAdminAccess } from '@/store/main/getters';
import { readReportRecords, readReportDate } from '@/store/report/getters';
import {
  dispatchGetReportRecords,
  dispatchSetReportDate,
} from '@/store/report/actions';
// import { api } from '@/api';

@Component
export default class Report extends Vue {
  public menu2 = false;

  public headers = [
    {
      text: 'Date',
      sortable: true,
      value: 'date',
      align: 'left',
    },
    {
      text: 'Time',
      sortable: true,
      value: 'time',
      align: 'left',
    },
    {
      text: 'Rx',
      sortable: true,
      value: 'rx',
      align: 'left',
    },
    {
      text: 'Tx',
      sortable: true,
      value: 'tx',
      align: 'left',
    },
    {
      text: 'Opco',
      value: 'opco',
    },
  ];
  get records() {
    return readReportRecords(this.$store);
  }

  get isAdmin() {
    return readHasAdminAccess(this.$store);
  }

  get date() {
    return readReportDate(this.$store).toISOString().substr(0, 10);
  }

  set date(dt: string) {
    dispatchSetReportDate(this.$store, new Date(dt));
  }

  public async mounted() {
    await dispatchGetReportRecords(this.$store);
  }
}
</script>
