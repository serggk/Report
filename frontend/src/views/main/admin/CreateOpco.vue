<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create Opco</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
            <v-text-field label="Company Name" v-model="name" required></v-text-field>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">
              Save
            </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  IOpcoRecord,
  IOpcoRecordCreate,
} from '@/interfaces';
import { dispatchCreateOpco, dispatchGetOpco, dispatchUpdateOpco } from '@/store/admin/actions';
import { readAdminOneOpco, readAdminOpco } from '@/store/admin/getters';
import router from '@/router';

const OpcoProps = Vue.extend({
  props: {
    isCreated: {default: true, type: Boolean},
  },
});

@Component
export default class CreateOpco extends OpcoProps {
  public valid = false;
  public opcoId: number = 0;
  public name: string = '';
  public readedOpco: IOpcoRecord|undefined = undefined;

  public async mounted() {
    await dispatchGetOpco(this.$store);
    if (this.isCreated) {
      this.reset();
    } else {
      this.readedOpco = readAdminOneOpco(this.$store)(+this.$router.currentRoute.params.id);
      this.opcoId = this.readedOpco!.id;
      this.name = this.readedOpco!.title;
    }
  }

  public reset() {
    if (this.isCreated) {
      this.name = '';
    } else {
      this.name = this.readedOpco!.title;
    }
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const createdOpco: IOpcoRecordCreate = {
        title: this.name,
      };
      const updatedOpco: IOpcoRecord = {
        id: this.opcoId,
        title: this.name,
      };
      if (this.isCreated) {
        await dispatchCreateOpco(this.$store, createdOpco).then(
          () => this.$router.push('/main/admin/opco'),
        ).catch();
      } else {
        await dispatchUpdateOpco(this.$store, {id: this.opcoId, opco: updatedOpco}).then(
          () => this.$router.push('/main/admin/opco'),
        ).catch();
      }
    }
  }
}
</script>
