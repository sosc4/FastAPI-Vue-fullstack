/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Types
import type { App } from 'vue'
import 'vue-toastification/dist/index.css'
import Toast, { PluginOptions } from 'vue-toastification'
import router from '../router'
import pinia from '../stores'
// Plugins
import vuetify from './vuetify'

const toastOptions: PluginOptions = {}

export function registerPlugins (app: App) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
    .use(Toast, toastOptions)
}
