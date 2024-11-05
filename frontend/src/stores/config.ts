import { AppConfig } from '@/interfaces'
import { defineStore } from 'pinia'

export const useConfig = defineStore('config', {
  state: (): { config: AppConfig | null } => ({ config: null }),
  actions: {
    setConfig (config: AppConfig) {
      this.config = config
    },
    clearConfig () {
      this.config = null
    },
  },
  persist: true,
})
