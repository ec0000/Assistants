// main.js
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import HomePage from './components/HomePage.vue'
import ChatAssistant from './components/ChatAssistant.vue'
import AssistantAdmin from './components/AssistantAdmin.vue'
import AboutUs from './components/AboutUs.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/chat', component: ChatAssistant },
  { path: '/admin', component: AssistantAdmin },
  { path: '/about', component: AboutUs },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')