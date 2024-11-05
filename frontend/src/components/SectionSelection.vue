<script lang="ts" setup>

  import { logout } from '@/functions'

  const emit = defineEmits(['select'])
  const props = defineProps<{
    current: string;
    lock: string | null;
  }>()
  const selectSetting = (setting: string) => {
    emit('select', setting)
  }

  const settings = [
    {
      icon: 'mdi-security',
      title: 'Hasło',
      setting: 'password',
    },
    {
      icon: 'mdi-account',
      title: 'Użytkownicy',
      setting: 'users',
    },
    {
      icon: 'mdi-lock',
      title: 'Bezpieczeństwo',
      setting: 'config',
    },
  ]

</script>

<template>
  <v-card
    class="settings-selection"
  >
    <v-list>
      <v-list-item
        v-for="setting in settings"
        v-show="!props.lock || setting.setting === props.lock"
        :key="setting"
        :class="{ 'text-primary': setting.setting === props.current }"
        @click="selectSetting(setting.setting)"
      >
        <template #prepend>
          <v-icon>
            {{ setting.icon }}
          </v-icon>
        </template>
        <span>
          {{ setting.title }}
        </span>
      </v-list-item>

      <v-list-item
        @click="logout"
      >
        <template #prepend>
          <v-icon>
            mdi-logout
          </v-icon>
        </template>
        <span>
          Wyloguj
        </span>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<style lang="scss" scoped>
.settings-selection {
  margin-right: 10px;
}
</style>
