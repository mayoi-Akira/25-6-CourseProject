// src/shims-element-plus.d.ts
import { ElMessage } from 'element-plus'
import type { User } from './types'
import 'vue'
import { Router, RouteLocationNormalizedLoaded } from 'vue-router'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $message: typeof ElMessage
    $router: Router
    $route: RouteLocationNormalizedLoaded
    user: User
  }
}
