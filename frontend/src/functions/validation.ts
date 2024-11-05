import { useConfig } from '@/stores/config'
import { computed } from 'vue'

export const usernameRules = [
  v => !!v || 'Nazwa użytkownika jest wymagana',
]

export const passwordRules = [
  v => !!v || 'Hasło jest wymagane',
]

export const newPasswordRules = computed(() => {
  const configStore = useConfig()
  const config = configStore.config

  const rules = [
    (v: string) => !!v || 'Hasło jest wymagane',
  ]

  if (config?.password_validation_enabled && config.password_min_length) {
    rules.push(
      (v: string) => v.length >= config.password_min_length || `Hasło musi mieć co najmniej ${config.password_min_length} znaków`
    )
  }

  if (config?.password_validation_enabled && config.password_require_digit) {
    rules.push(
      (v: string) => /\d/.test(v) || 'Hasło musi zawierać co najmniej jedną cyfrę'
    )
  }

  if (config?.password_validation_enabled && config.password_require_special) {
    rules.push(
      (v: string) => /[!@#$%^&*()_\-+=\[\]{};:'"\\|,.<>?/~`]/.test(v) || 'Hasło musi zawierać co najmniej jeden znak specjalny'
    )
  }

  return rules
})

export const nonNegativeRule = (v: number) => v >= 0 || 'Wartość nie może być ujemna'
