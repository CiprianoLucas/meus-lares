export default [
    {
        path: '/fatura/relacao/cadastro',
        name: 'relacao-fatura-cadastro',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de relacionamento de fatura" */ './pages/RelationInvoiceRegister.vue'
            )
    },
    {
        path: '/fatura/relacao/:id',
        name: 'relacao-fatura-atualizar',
        component: () =>
            import(
                /* webpacjChunkName: "cadastro de relacionamento de fatura" */ './pages/RelationInvoiceRegister.vue'
            )
    },
    {
        path: '/fatura/relacao-lista',
        name: 'relacao-fatura-lista',
        component: () =>
            import(
                /* webpacjChunkName: "lista de relacionamento das fatura" */ './pages/RelationInvoicelist.vue'
            )
    },
    {
        path: '/fatura/lista/',
        name: 'fatura-lista',
        component: () =>
            import(/* webpacjChunkName: "lista de faturas" */ './pages/InvoiceList.vue')
    }
]
