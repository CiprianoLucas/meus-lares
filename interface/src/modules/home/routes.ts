export default [
    {
        path: '/',
        name: 'home',
        component: () => import(/* webpackChunkName: "home" */ './pages/HomePage.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/proprietario',
        name: 'home-owner',
        component: () => import(/* webpackChunkName: "home proprietario" */ './pages/OwnerHomePage.vue'),
        meta: { requiresAuth: false }
    }
]
