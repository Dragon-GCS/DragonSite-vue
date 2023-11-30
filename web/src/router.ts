import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  { path: '/', redirect: { name: 'home', query: { personal: 'false' } } },
  { path: '/home', name: 'home', component: () => import('./views/Main.vue') },
  { path: '/login', name: 'login', component: () => import('./views/Login.vue') },
  { path: '/preview', name: 'preview', component: () => import('./views/Preview.vue') },
  { path: '/:path(.*)', name: 'NotFound', component: () => import('./views/NotFound.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
