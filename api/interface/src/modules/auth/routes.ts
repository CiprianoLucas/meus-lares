export default [
    {
        path: '/login',
        name: 'login',
        component: () => import(/* webpacjChunkName: "login" */ './pages/UserLogin.vue')
    }
]