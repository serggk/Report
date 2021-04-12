<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Upload Report File</div>
      </v-card-title>
      <v-card-text>
        <v-file-input chips show-size counter @change="changeFile"></v-file-input>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn
          @click="submit"
          :disabled="!valid"
        >
          Upload
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { api } from '@/api';
import { readToken } from '@/store/main/getters';


@Component
export default class ReportUploadFile extends Vue {
  public valid = true;
  public file;

  public changeFile(file: File[]) {
    this.file = file;
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    const formData = new FormData();
    if (this.file) {
      formData.append('file', this.file);
      await api.uploadReport(formData, readToken(this.$store));
      this.$router.push('/main/report');
    }
  }
}
</script>
