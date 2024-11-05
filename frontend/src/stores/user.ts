import { Api } from '@/api/api'
import { ApiCore } from '@/api/core'
import { UserResponse } from '@/interfaces'
import { defineStore } from 'pinia'

export const useUser = defineStore('user', {
  state: (): { user: UserResponse | null } => ({ user: null }),
  actions: {
    setUser (user: UserResponse) {
      this.user = user
    },
    clearUser () {
      this.user = null
    },
    async fetchMe () {
      const api = Api.getInstance()

      try {
        const user = await api.readMe()
        this.setUser(user)
      } catch (error) {
        this.clearUser()
        throw error
      }
    },
    async logout () {
      ApiCore.clearToken()
      this.clearUser()

      location.reload()
    },
  },
  persist: true,
})
