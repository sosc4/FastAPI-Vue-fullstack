<script lang="ts" setup>
  import { Api } from '@/api/api'
  import { banUser, createUser, deleteUser, suChangePassword, suChangeUsername, unbanUser } from '@/functions'
  import { newPasswordRules, usernameRules } from '@/functions/validation'
  import { UserResponse } from '@/interfaces'
  import { onMounted, ref } from 'vue'

  const modal = ref(false)
  const selectedUserId = ref<null | number>(null)

  const valid = ref(false)
  const username = ref('')
  const password = ref('')

  const users = ref<UserResponse[]>([])

  async function readUsers () {
    const api = Api.getInstance()

    users.value = await api.readAllUsers()
  }

  async function newUser ({
    username,
    password,
  }) {
    await createUser({
      username,
      password,
    })

    await readUsers()
  }

  async function delUser (id: number) {
    await deleteUser(id)
    await readUsers()
  }

  async function ban (id: number) {
    await banUser(id)
    users.value = users.value.map(user => {
      if (user.id === id) {
        user.is_active = false
      }

      return user
    })
  }

  async function unban (id: number) {
    await unbanUser(id)
    users.value = users.value.map(user => {
      if (user.id === id) {
        user.is_active = true
      }

      return user
    })
  }

  async function updateUsername (id: number, username: string) {
    await suChangeUsername(id, username)
    users.value = users.value.map(user => {
      if (user.id === id) {
        user.username = username
      }

      return user
    })
    modal.value = false
  }

  async function updatePassword (id: number, password: string) {
    await suChangePassword(id, password)
    await readUsers()
    modal.value = false
  }

  onMounted(async () => {
    await readUsers()
  })
</script>

<template>
  <v-container>
    <v-form
      v-model="valid"
      @submit.prevent="newUser({
        username: username,
        password: password
      })"
    >
      <v-row>
        <v-col>
          <v-text-field
            v-model="username"
            label="Nazwa użytkownika"
            required
            :rules="usernameRules"
            type="text"
          />
        </v-col>
        <v-col>
          <v-text-field
            v-model="password"
            label="Hasło"
            required
            :rules="newPasswordRules"
            type="password"
          />
        </v-col>
        <v-col>
          <v-btn
            color="primary"
            :disabled="!valid"
            prepend-icon="mdi-plus"
            type="submit"
          >
            Dodaj użytkownika
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <v-row>
      <v-progress-circular v-if="users.length === 0" indeterminate />
      <users-list
        v-else
        :users="users"
        @ban="ban($event)"
        @delete="delUser($event)"
        @edit="selectedUserId = $event; modal = true"
        @unban="unban($event)"
      />
    </v-row>
  </v-container>

  <update-user-modal
    v-model="modal"
    :user-id="selectedUserId"
    @close="modal = false"
    @update:password="updatePassword($event.id, $event.password)"
    @update:username="updateUsername($event.id, $event.username)"
  />

</template>

<style lang="scss" scoped>

</style>
