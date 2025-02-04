export default [
    {
        path: '/usuario/', //don't forget insert in router folder
        name: 'pagina-usuario',
        component: () => import(/* webpacjChunkName: "página do usuário" */ './pages/UserPage.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/usuario/cadastro/', //don't forget insert in router folder
        name: 'cadastro_usuario',
        component: () =>
            import(/* webpacjChunkName: "cadastro de usuário" */ './pages/UserRegister.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/usuario/papel/', //don't forget insert in router folder
        name: 'escolha-perfil',
        component: () =>
            import(/* webpacjChunkName: "escolha de perfil" */ './pages/ChoiceRole.vue')
    }
]
