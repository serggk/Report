<template>
  <div>
    <v-app-bar light>
      <v-app-bar-title>
        Manage Users
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-app-bar>
    <v-data-table :headers="headers" :items="users">
      <template v-slot:item.isActive="{ item }">
        <v-simple-checkbox
          v-model="item.is_active"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:item.isSuperuser="{ item }">
        <v-simple-checkbox
          v-model="item.is_superuser"
          disabled
        ></v-simple-checkbox>
      </template>
      <template v-slot:item.id="{ item }">
        <v-btn slot="activator" text :to="{name: 'main-admin-users-edit', params: {id: item.id}}">
          <v-icon>edit</v-icon>
        </v-btn>
      </template>      
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { IUserProfile } from '@/interfaces';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';

@Component
export default class AdminUsers extends Vue {
  public headers = [
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'Full Name',
      sortable: true,
      value: 'full_name',
      align: 'left',
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'isActive',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'isSuperuser',
      align: 'left',
    },
    {
      text: 'Opco',
      sortable: true,
      value: 'opco.title',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>
