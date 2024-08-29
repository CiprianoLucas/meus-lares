export default [
    {
        path: '/condominio/cadastro',
        name: 'condominio_cadastro', 
        component: () => import(/* webpacjChunkName: "cadastro de condomínio" */ './pages/PlaceRegister.vue')
    },
    {
        path: '/condominio/lista',
        name: 'condominio_lista', 
        component: () => import(/* webpacjChunkName: "lista de condomínios" */ './pages/PlaceList.vue')
    },
    {
        path: '/condominio/:id',
        name: 'condominio_editar', 
        component: () => import(/* webpacjChunkName: "Edição de condomínio" */ './pages/PlaceRegister.vue')
    },
    {
        path: '/condominio/:id/sindicos',
        name: 'condominio_sindicos', 
        component: () => import(/* webpacjChunkName: "Listagem de síndicos" */ './pages/PlaceUnions.vue')
    },
    {
        path: '/condominio/:id/moradores',
        name: 'condominio_moradores', 
        component: () => import(/* webpacjChunkName: "Listagem de moradores" */ './pages/PlaceResidents.vue')
    },
]