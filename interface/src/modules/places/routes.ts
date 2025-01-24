export default [
    {
        path: '/condominio/cadastro/',
        name: 'condominio_cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de condomínio" */ './pages/CondominiumRegisterUpdate.vue'
            )
    },
    {
        path: '/condominio/edicao/:id/',
        name: 'condominio_edicao',
        component: () =>
            import(
                /* webpacjChunkName: "edição de condomínio" */ './pages/CondominiumRegisterUpdate.vue'
            )
    },
    {
        path: '/condominio/lista/',
        name: 'condominio_lista',
        component: () =>
            import(/* webpacjChunkName: "lista de condomínios" */ './pages/CondominiumList.vue')
    },
    {
        path: '/condominio/:id/',
        name: 'condominio_page',
        component: () =>
            import(/* webpacjChunkName: "página do condomínio" */ './pages/CondominiumPage.vue')
    },
    {
        path: '/apartamento/cadastro/',
        name: 'apartamento_cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de apartamento" */ './pages/ApartmentRegisterUpdate.vue'
            )
    },
    {
        path: '/apartamento/edicao/:id/',
        name: 'apartamento_edicao',
        component: () =>
            import(
                /* webpacjChunkName: "edição de apartamento" */ './pages/ApartmentRegisterUpdate.vue'
            )
    },
    {
        path: '/apartamento/:id/',
        name: 'apartamento_page',
        component: () =>
            import(/* webpacjChunkName: "página do apartamento" */ './pages/ApartmentPage.vue')
    },
    {
        path: '/estacionamento/cadastro/',
        name: 'estacionamento_cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de estacionamento" */ './pages/ParkRegisterUpdate.vue'
            )
    },
    {
        path: '/estacionamento/edicao/:id/',
        name: 'estacionamento_edicao',
        component: () =>
            import(
                /* webpacjChunkName: "edição de estacionamento" */ './pages/ParkRegisterUpdate.vue'
            )
    },
    {
        path: '/estacionamento/:id/',
        name: 'estacionamento_page',
        component: () =>
            import(/* webpacjChunkName: "página do estacionamento" */ './pages/CondominiumPage.vue')
    },
    {
        path: '/espaco-compartilhado/cadastro/',
        name: 'espaco-compartilhado_cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de espaço compartilhado" */ './pages/SharedPlaceRegisterUpdate.vue'
            )
    },
    {
        path: '/espaco-compartilhado/edicao/:id/',
        name: 'espaco-compartilhado_edicao',
        component: () =>
            import(
                /* webpacjChunkName: "edição de espaço compartilhado" */ './pages/SharedPlaceRegisterUpdate.vue'
            )
    },
    {
        path: '/espaco-compartilhado/:id/',
        name: 'espaco-compartilhado_page',
        component: () =>
            import(
                /* webpacjChunkName: "página do espaço compartilhado" */ './pages/CondominiumPage.vue'
            )
    }
]
