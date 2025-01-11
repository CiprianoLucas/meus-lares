export default [
    {
        path: '/condominio/cadastro',
        name: 'condominio_cadastro',
        component: () =>
            import(/* webpacjChunkName: "cadastro de condomínio" */ './pages/CondominiumRegister.vue')
    },
    {
        path: '/condominio/lista',
        name: 'condominio_lista',
        component: () =>
            import(/* webpacjChunkName: "lista de condomínios" */ './pages/CondominiumList.vue')
    },
    {
        path: '/condominio/:id',
        name: 'condominio_editar',
        component: () =>
            import(/* webpacjChunkName: "Edição de condomínio" */ './pages/CondominiumUpdate.vue')
    }
]
