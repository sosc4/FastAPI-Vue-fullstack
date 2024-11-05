import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { ApiCore } from '../api/core'
import { routes as staticRoutes } from './statics'

const routes: RouteRecordRaw[] = []
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes.concat(
    staticRoutes,
  ),
})

router.beforeEach((to, from, next) => {
  window.document.title = (to.meta && to.meta.title ? to.meta.title : 'Home')

  if (to.name === 'login' && ApiCore.isLoggedIn) {
    return next({ name: 'home' })
  }

  if (to.meta.requiresAuth) {
    if (!ApiCore.isLoggedIn) {
      return next({ name: 'login' })
    }
  }

  next()
})

export default router
