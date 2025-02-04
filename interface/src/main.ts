import { createPinia } from 'pinia'
import '@/assets/scss/app.scss'
import '../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import App from '@/App.vue'
import router from '@/router'
import { Tooltip } from 'bootstrap'

const pinea = createPinia()
pinea.use(piniaPluginPersistedstate)

const app = createApp(App)
app.use(pinea)
app.use(router)
app.mount('#app')
