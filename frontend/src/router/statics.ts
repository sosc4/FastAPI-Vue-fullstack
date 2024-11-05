import { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    meta: {
      requiresAuth: true,
      title: 'Home',
    },
    component: () => import('../pages/HomePage.vue'),
  },
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login',
    },
    component: () => import('../pages/LoginPage.vue'),
  },
]
