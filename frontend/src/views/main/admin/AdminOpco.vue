<template>
  <div>
    <v-app-bar light>
      <v-app-bar-title>
        Manage Companies
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/opco/create">Create OpCo</v-btn>
    </v-app-bar>
    <v-data-table :headers="headers" :items="opco">
      <template v-slot:item.id="{ item }">
        <v-btn slot="activator" text :to="{name: 'main-admin-opco-edit', params: {id: item.id}}">
          <v-icon>edit</v-icon>
        </v-btn>
        <v-btn slot="activator" text @click="deleteOpco(item.id)">
          <v-icon>delete</v-icon>
        </v-btn>
      </template>      
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readAdminOpco } from '@/store/admin/getters';
import { dispatchDeleteOpco, dispatchGetOpco } from '@/store/admin/actions';

@Component
export default class AdminOpco extends Vue {
  public headers = [
    {
      text: 'Nane',
      sortable: true,
      value: 'title',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];
  get opco() {
    return readAdminOpco(this.$store);
  }

  public async mounted() {
    await dispatchGetOpco(this.$store);
  }

  public async deleteOpco(opcoId: number) {
    await dispatchDeleteOpco(this.$store, opcoId);
  }
}
</script>
