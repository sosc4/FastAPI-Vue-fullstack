import { Api } from '@/api/api'
import { AppConfigUpdate, PasswordChange, UserCreate } from '@/interfaces'
import { useConfig } from '@/stores/config'
import { useUser } from '@/stores/user'
import { useToast } from 'vue-toastification'

export async function logout () {
  const api = Api.getInstance()
  const userStore = useUser()

  await api.logout()
  await userStore.logout()
}

export async function changePassword (data: PasswordChange) {
  const api = Api.getInstance()
  const userStore = useUser()
  const toast = useToast()

  const response = await api.changePassword(data)

  toast.success('Hasło zostało zmienione')

  userStore.setUser(response)
  return response
}

export async function createUser (data: UserCreate) {
  const api = Api.getInstance()
  const toast = useToast()

  const response = await api.createUser(data)

  toast.success('Użytkownik został utworzony')

  return response
}

export async function banUser (id: number) {
  const api = Api.getInstance()
  const toast = useToast()

  await api.updateUser(id, { is_active: false })

  toast.success('Użytkownik został zbanowany')
}

export async function unbanUser (id: number) {
  const api = Api.getInstance()
  const toast = useToast()

  await api.updateUser(id, { is_active: true })

  toast.success('Użytkownik został odbanowany')
}

export async function deleteUser (id: number) {
  const api = Api.getInstance()
  const toast = useToast()

  await api.deleteUser(id)

  toast.success('Użytkownik został usunięty')
}

export async function suChangeUsername (id: number, username: string) {
  const api = Api.getInstance()
  const toast = useToast()

  await api.updateUser(id, { username })

  toast.success('Nazwa użytkownika została zmieniona')
}

export async function suChangePassword (id: number, password: string) {
  const api = Api.getInstance()
  const toast = useToast()

  await api.updateUser(id, { password })

  toast.success('Hasło zostało zmienione')
}

export async function getConfig () {
  const api = Api.getInstance()
  const configStore = useConfig()

  const config = await api.getConfig()

  configStore.setConfig(config)
}

export async function updateConfig (data: AppConfigUpdate) {
  const api = Api.getInstance()
  const configStore = useConfig()
  const toast = useToast()

  const config = await api.updateConfig(data)

  toast.success('Konfiguracja została zaktualizowana')

  configStore.setConfig(config)
}

export async function toggleConfigPasswordValidation () {
  const api = Api.getInstance()
  const configStore = useConfig()
  const toast = useToast()

  const config = await api.toggleConfigPasswordValidation()
  configStore.setConfig(config)

  const state = config.password_validation_enabled ? 'włączona' : 'wyłączona'
  toast.success(`Walidacja hasła została ${state}`)
}
