<script lang="ts" setup>
  import { useUser } from '@/stores/user'
  import { ref } from 'vue'

  const userStore = useUser()
  const currentSection = ref('password')

  const selectSetting = (setting: string) => {
    currentSection.value = setting
  }

  const lock = computed(() => {
    const user = userStore.user

    if (!user) return null

    if (!user.is_admin) {
      return 'password'
    }

    if (user.force_password_change) {
      return 'password'
    }

    return null
  })

</script>

<template>
  <v-container
    max-width="auto"
  >
    <v-row>
      <v-col
        :cols="3"
      >
        <section-selection
          :current="currentSection"
          :lock="lock"
          @select="selectSetting"
        />
      </v-col>
      <v-col
        :cols="9"
      >
        <section-card
          :section="currentSection"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>
