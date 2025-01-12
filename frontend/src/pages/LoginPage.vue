<script lang="ts" setup>
  import { ApiCore } from '@/api/core'
  import { getConfig } from '@/functions'
  import { passwordRules, usernameRules } from '@/functions/validation'
  import { useUser } from '@/stores/user'
  import { ref } from 'vue'
  import { useToast } from 'vue-toastification'
  import router from '../router'

  const username = ref('')
  const password = ref('')
  const valid = ref(false)

  const useOtp = ref<boolean>(false)
  const x = ref<number | undefined>(undefined)
  const a = ref<number | undefined>(undefined)

  function toggleOtp() {
    useOtp.value = !useOtp.value

    if (useOtp.value) {
      x.value = Math.floor(Math.random() * 10) + 1
      a.value = Math.floor(Math.random() * 10) + 1
    } else {
      x.value = undefined
      a.value = undefined
    }
  }

  async function login () {
    const userStore = useUser()
    const toast = useToast()
    const apiCore = ApiCore.getInstance()

    await apiCore.login({
      username: username.value,
      password: password.value,
      x: x.value,
      a: a.value,
    })

    if (!ApiCore.isLoggedIn) {
      return
    }

    await userStore.fetchMe()
    await getConfig()

    toast.info('Zalogowano pomyślnie. Witaj ponownie, ' + userStore.user?.username + '!')

    await router.push({ name: 'home' })
  }


</script>

<template>
  <v-card
    class="mx-auto mt-16"
    max-width="400"
  >
    <v-card-title>
      Zaloguj się
    </v-card-title>
    <v-card-item>
      <v-form
        v-model="valid"
        @submit.prevent="login"
      >
        <v-text-field
          v-model="username"
          label="Nazwa użytkownika"
          required
          :rules="usernameRules"
          type="text"
        />

        <v-text-field
          v-model="password"
          label="Hasło"
          required
          :rules="passwordRules"
          type="password"
          append-inner-icon="mdi-lock-clock"
          @click:append-inner="toggleOtp"
        />

        <v-row v-if="useOtp">
          <v-col>
            x: {{ x }} a: {{ a }}
          </v-col>
        </v-row>

        <v-btn
          block
          class="mr-4"
          color="primary"
          :disabled="!valid"
          type="submit"
        >
          Zaloguj
        </v-btn>
      </v-form>
    </v-card-item>
  </v-card>
</template>

<style scoped>

</style>
