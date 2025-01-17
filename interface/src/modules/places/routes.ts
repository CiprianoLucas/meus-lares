export default [
    {
        path: '/condominio/cadastro',
        name: 'condominio_cadastro',
        component: () =>
            import(/* webpacjChunkName: "cadastro de condomínio" */ './pages/CondominiumRegisterUpdate.vue')
    },
    {
        path: '/condominio/edicao/:id',
        name: 'condominio_edicao',
        component: () =>
            import(/* webpacjChunkName: "edição de condomínio" */ './pages/CondominiumRegisterUpdate.vue')
    },
    {
        path: '/condominio/lista',
        name: 'condominio_lista',
        component: () =>
            import(/* webpacjChunkName: "lista de condomínios" */ './pages/CondominiumList.vue')
    },
    {
        path: '/condominio/:id',
        name: 'condominio_page',
        component: () =>
            import(/* webpacjChunkName: "página do condomínio" */ './pages/CondominiumPage.vue')
    }
]
