export default [
    {
        path: '/condominio/cadastro', //don't forget insert in router folder
        name: 'condominio_cadastro', 
        component: () => import(/* webpacjChunkName: "cadastro de condomínio" */ './pages/PlaceRegister.vue')
    }
]