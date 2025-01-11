<script lang="ts" setup>
  import ConfigSettings from '@/components/ConfigSettings.vue'
  import PasswordSettings from '@/components/PasswordSettings.vue'
  import UsersSettings from '@/components/UsersSettings.vue'
  import { useUser } from '@/stores/user'
  import { computed } from 'vue'
  import LogSettings from "@/components/LogSettings.vue";

  const userStore = useUser()

  const props = defineProps<{
    section: string;
  }>()

  const sectionMapping = {
    password: {
      title: computed(() => userStore.user?.force_password_change ? 'Wymagana zmiana hasła' : 'Ustawienia hasła'),
      component: PasswordSettings,
    },
    users: {
      title: ref('Zarządzanie użytkownikami'),
      component: UsersSettings,
    },
    config: {
      title: ref('Bezpieczeństwo'),
      component: ConfigSettings,
    },
    activity: {
      title: ref('Dziennik aktywności'),
      component: LogSettings,
    }
  }

  const currentSection = computed(() => {
    if (props.section && props.section in sectionMapping) {
      return sectionMapping[props.section]
    } else {
      return { title: 'Ładowanie' }
    }
  })
</script>

<template>
  <v-card
    color="surface"
  >
    <v-card-title
      class="modal-title"
    >
      <span class="card-title">
        {{ currentSection.title.value }}
      </span>
    </v-card-title>

    <v-divider />

    <v-card-item>
      <component :is="currentSection.component" />
    </v-card-item>
  </v-card>
</template>

<style lang="scss" scoped>

</style>
