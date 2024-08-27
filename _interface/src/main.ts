import { createPinia } from 'pinia'
import '@/assets/scss/app.scss'
import { createApp } from 'vue'
import router from '@/router'
import App from '@/App.vue'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

//DON'T CHANGE THIS FILE