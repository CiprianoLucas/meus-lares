export default [
    {
        path: '/morador/cadastro/',
        name: 'morador-cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de morador em apartamento" */ './pages/RegisterCondoTenant.vue'
            )
    }
]
