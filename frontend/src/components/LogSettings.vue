<script lang="ts" setup>
import {ref} from 'vue'
import {LogResponse} from "@/interfaces";
import {Api} from "@/api/api";
import LogList from "@/components/LogList.vue";

const logs = ref<LogResponse[]>([]);

async function readLogs() {
  const api = Api.getInstance();

  logs.value = await api.readAllLogs();
}

onMounted(() => {
  readLogs();
});
</script>

<template>
  <v-card>
    <log-list :logs="logs" />
  </v-card>
</template>