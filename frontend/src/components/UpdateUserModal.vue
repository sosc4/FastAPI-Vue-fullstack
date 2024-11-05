<script lang="ts" setup>
  import { newPasswordRules, usernameRules } from '@/functions/validation'
  import { defineEmits, defineProps, ref, watch } from 'vue'

  const props = defineProps({
    value: Boolean,
    userId: Number,
  })

  const emit = defineEmits(['close', 'update:username', 'update:password'])

  const dialog = ref(props.value)
  watch(() => props.value, newVal => {
    dialog.value = newVal
  })

  const validUsername = ref(false)
  const validPassword = ref(false)
  const newUsername = ref('')
  const newPassword = ref('')

  const close = () => {
    dialog.value = false
    emit('close')
  }

  const saveUsername = () => {
    if (validUsername.value) {
      emit('update:username', {
        id: props.userId,
        username: newUsername.value,
      })
    }
  }

  const savePassword = () => {
    if (validPassword.value) {
      emit('update:password', {
        id: props.userId,
        password: newPassword.value,
      })
    }
  }
</script>

<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-form v-model="validUsername" @submit.prevent="saveUsername">
        <v-card-title>
          Zmień nazwę użytkownika
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newUsername"
            label="New Username"
            required
            :rules="usernameRules"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="secondary"
            :disabled="!validUsername"
            type="submit"
          >
            Zapisz nazwę użytkownika
          </v-btn>
        </v-card-actions>
      </v-form>

      <v-form
        v-model="validPassword"
        class="mt-4"
        @submit.prevent="savePassword"
      >
        <v-card-title>
          Zmień hasło
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="newPassword"
            label="New Password"
            required
            :rules="newPasswordRules"
            type="password"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="secondary"
            :disabled="!validPassword"
            type="submit"
          >
            Zapisz hasło
          </v-btn>
        </v-card-actions>
      </v-form>

      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="close">
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
