import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  { path: "/", redirect: {name: 'main', query: { path: '/', logRequire: 'false'}} },
  {
    path: '/home',
    name: 'main',
    component: () => import(/* webpackChunkName: "view" */   './views/MainView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "view" */   './views/Login.vue'),
  },
  {
    path: '/preview',
    name: 'preview',
    component: () => import(/* webpackChunkName: "view" */   './views/Preview.vue'),
    props: true
  },
  // {
  //   path: '/:path(.*)',
  //   name: 'NotFound',
  //   component: () => import(/* webpackChunkName: "view" */   './views/NotFound.vue'),
  // },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
