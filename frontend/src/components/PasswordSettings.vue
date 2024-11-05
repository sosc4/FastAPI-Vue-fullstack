<script lang="ts" setup>
  import { changePassword } from '@/functions'
  import { newPasswordRules, passwordRules } from '@/functions/validation'
  import { useUser } from '@/stores/user'

  const formattedPasswordExpires = computed(() => {
    const userStore = useUser()
    if (!userStore.user?.password_expires) return ''
    const date = new Date(userStore.user.password_expires)
    return date.toISOString().split('T')[0] // Returns "YYYY-MM-DD"
  })

  const valid = ref(false)

  const oldPassword = ref('')
  const newPassword = ref('')
</script>

<template>

  <span>
    Twoje hasło wygasa: {{ formattedPasswordExpires }}
  </span>

  <v-form
    v-model="valid"
    @submit.prevent="changePassword({old_password: oldPassword, new_password: newPassword})"
  >
    <v-text-field
      v-model="oldPassword"
      label="Stare hasło"
      required
      :rules="passwordRules"
      type="password"
    />

    <v-text-field
      v-model="newPassword"
      label="Nowe hasło"
      required
      :rules="newPasswordRules"
      type="password"
    />

    <v-btn
      color="primary"
      :disabled="!valid"
      prepend-icon="mdi-pencil"
      type="submit"
    >
      Zmień hasło
    </v-btn>
  </v-form>
</template>
<style lang="scss" scoped>

</style>
