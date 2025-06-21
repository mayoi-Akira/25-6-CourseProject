// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { hide: true },
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
  },
  // 其他路由可以在这里继续添加
]

const router = createRouter({
  history: createWebHistory(), // HTML5 模式
  routes,
})

export default router
