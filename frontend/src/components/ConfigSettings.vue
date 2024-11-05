<script lang="ts" setup>
  import { toggleConfigPasswordValidation, updateConfig } from '@/functions'
  import { nonNegativeRule } from '@/functions/validation'
  import { useConfig } from '@/stores/config'
  import { ref } from 'vue'

  const configStore = useConfig()

  const passwordLength = ref(configStore.config.password_min_length)
  const passwordRequireDigit = ref(configStore.config.password_require_digit)
  const passwordRequireSpecial = ref(configStore.config.password_require_special)
  const passwordExpires = ref(configStore.config.password_expire_days)

</script>

<template>
  <v-container>
    <v-row>
      Walidacja hasła
    </v-row>
    <v-row>
      <h5>
        Walidacja hasła jest aktualnie
        <b class="text-primary">
          {{ configStore.config.password_validation_enabled ? 'włączona.' : 'wyłączona.' }}
        </b>
      </h5>
    </v-row>
    <v-row>
      <v-btn
        :color="[
          configStore.config.password_validation_enabled ? 'error' : 'success'
        ]"
        @click="toggleConfigPasswordValidation"
      >
        {{ configStore.config.password_validation_enabled ? 'Wyłącz walidację hasła' : 'Włącz walidację hasła' }}
      </v-btn>
    </v-row>
  </v-container>
  <v-container>
    <v-form
      @submit.prevent="updateConfig({
        password_min_length: passwordLength,
        password_require_digit: passwordRequireDigit,
        password_require_special: passwordRequireSpecial,
        password_expire_days: passwordExpires
      })"
    >
      <v-row>
        <h4>Minimalna długość i złożoność hasła dla użytkownika</h4>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="passwordLength"
            label="Minimalna długość hasła"
            required
            type="number"
          />
        </v-col>
        <v-col>
          <v-checkbox
            v-model="passwordRequireDigit"
            label="Wymagaj cyfry"
          />
        </v-col>
        <v-col>
          <v-checkbox
            v-model="passwordRequireSpecial"
            label="Wymagaj znaku specjalnego"
          />
        </v-col>
      </v-row>
      <v-row>
        <h4>Ważność hasła użytkownika</h4>
      </v-row>
      <v-row>

        <v-text-field
          v-model="passwordExpires"
          label="Ważność hasła w dniach"
          min="1"
          :rules="nonNegativeRule"
          type="number"
        />
      </v-row>
      <v-row>
        <v-btn
          color="primary"
          prepend-icon="mdi-pencil"
          type="submit"
        >
          Zaktualizuj konfigurację
        </v-btn>
        <v-row />
      </v-row>
    </v-form>
  </v-container>
</template>

<style lang="scss" scoped>

</style>
