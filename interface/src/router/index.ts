import { createRouter, createWebHistory } from 'vue-router'
import { routes } from './routes'
import { userStore } from '@/modules/user/stores'

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const user = userStore()
    const isAuthenticated = Boolean(user.username)

    const requiresAuth = to.meta.requiresAuth !== false

    if (requiresAuth && !isAuthenticated) {
        return next('/login')
    }

    next()
})

export default router
