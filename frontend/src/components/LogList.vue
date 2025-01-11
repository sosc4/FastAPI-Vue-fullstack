<script setup lang="ts">
import {LogResponse} from "@/interfaces";

const props = defineProps<{
  logs: LogResponse[];
}>();

function convertLogEventToPolish(event: string): string {
  const eventTranslations: Record<string, string> = {
    login: "Logowanie",
    logout: "Wylogowanie",
    password_change: "Zmiana hasła",
    user_added: "Dodano użytkownika",
    user_updated: "Zaktualizowano użytkownika",
    user_deleted: "Usunięto użytkownika",
    config_updated: "Zaktualizowano konfigurację",
  };

  return eventTranslations[event] || "Nieznane zdarzenie";
}
</script>

<template>
  <v-table>
    <thead>
    <tr>
      <th
          v-for="header in [
            'Użytkownik', 'Zdarzenie', 'Status', 'Wiadomość', 'Data'
        ]"
      >
        {{ header }}
      </th>
    </tr>
    </thead>
    <tbody>
    <tr
        v-for="log in props.logs"
        :key="log.id"
    >
      <td>
        {{ log.user_id }}
      </td>
      <td>
        {{ convertLogEventToPolish(log.event) }}
      </td>
      <td>
        <v-icon
            :color="log.status === 'success' ? 'success' : 'error'"
            :icon="log.status === 'success' ? 'mdi-check' : 'mdi-close'"
        />
      </td>
      <td>
        {{ log.message }}
      </td>
      <td>
        {{ log.created_at }}
      </td>
    </tr>
    </tbody>
  </v-table>
</template>

<style scoped lang="scss">

</style>