export default [
    {
        path: '/',
        name: 'home',
        component: () => import(/* webpackChunkName: "login" */ './pages/HomePage.vue')
    }
]
