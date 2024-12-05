export default [
    {
        path: '/usuario/cadastro/', //don't forget insert in router folder
        name: 'cadastro_usuario',
        component: () =>
            import(/* webpacjChunkName: "cadastro de usuário" */ './pages/UserRegister.vue')
    }
]
