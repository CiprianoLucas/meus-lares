export default [
    {
        path: '/requisicao/cadastro', //don't forget insert in router folder
        name: 'requisicao_cadastro',
        component: () =>
            import(/* webpacjChunkName: "cadastro de requisicao" */ './pages/RequestRegister.vue')
    },
    {
        path: '/requisicao/:id', //don't forget insert in router folder
        name: 'requisicao_editar',
        component: () =>
            import(/* webpacjChunkName: "Edição de requisicao" */ './pages/RequestRegister.vue')
    },
    {
        path: '/requisicao/pendentes', //don't forget insert in router folder
        name: 'requisicao_pendentes',
        component: () =>
            import(
                /* webpacjChunkName: "listar requisições pendentes" */ './pages/RequestListPendents.vue'
            )
    },
    {
        path: '/requisicao/capturados', //don't forget insert in router folder
        name: 'requisicao_capturados',
        component: () =>
            import(
                /* webpacjChunkName: "listar requisições capturados" */ './pages/RequestListCaptureds.vue'
            )
    },
    {
        path: '/requisicao/minhas-requisicoes', //don't forget insert in router folder
        name: 'requisicao_minhas_requisicoes',
        component: () =>
            import(/* webpacjChunkName: "listar minhas requisições" */ './pages/RequestListMy.vue')
    }
]
