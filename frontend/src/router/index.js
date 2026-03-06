import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/user'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', component: () => import('../pages/login/index.vue') },
  { path: '/home', component: () => import('../pages/home/index.vue'), meta: { auth: true } },
  { path: '/capture', component: () => import('../pages/capture/index.vue'), meta: { auth: true } },
  { path: '/thought/detail', component: () => import('../pages/thought/detail.vue'), meta: { auth: true } },
  { path: '/review', component: () => import('../pages/review/index.vue'), meta: { auth: true } },
  { path: '/review/detail', component: () => import('../pages/review/detail.vue'), meta: { auth: true } },
  { path: '/card', component: () => import('../pages/card/index.vue'), meta: { auth: true } },
  { path: '/card/create', component: () => import('../pages/card/create.vue'), meta: { auth: true } },
  { path: '/settings', component: () => import('../pages/settings/index.vue'), meta: { auth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const userStore = useUserStore()
  if (to.meta.auth && !userStore.isLoggedIn) {
    return '/login'
  }
})

export default router
