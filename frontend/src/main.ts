import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import ElementPlus from 'element-plus'

import App from './App.vue'

import './styles/main.css'
import 'uno.css'
import 'element-plus/dist/index.css'

const app = createApp(App)

const router = createRouter({
  routes,
  history: createWebHistory(import.meta.env.BASE_URL),
})

app.use(ElementPlus)
app.use(router)

app.mount('#app')
