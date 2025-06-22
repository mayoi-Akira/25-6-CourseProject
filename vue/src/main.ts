import './assets/main.css'

import { createApp, reactive } from 'vue'
import App from './App.vue'
import 'element-plus/dist/index.css'
import router from './router'
import ElementPlus from 'element-plus'
import '@/assets/global.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router)
app.use(ElementPlus, { size: 'small', zIndex: 3000 })

const user = reactive({ name: '111', role: '' })
app.provide('user', user)

app.mount('#app')
