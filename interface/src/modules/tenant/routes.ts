export default [
    {
        path: '/morador/cadastro/',
        name: 'morador-cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de morador em apartamento" */ './pages/CondoTenantRegister.vue'
            )
    },
    {
        path: '/morador/:id/',
        name: 'morador-pagina',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de morador em apartamento" */ './pages/CondoTenantPage.vue'
            )
    }
]
