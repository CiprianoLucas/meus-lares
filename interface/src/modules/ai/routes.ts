export default [
    {
        path: '/ai', //don't forget insert in router folder
        name: 'ai', 
        component: () => import(/* webpacjChunkName: "ai" */ './pages/AiChat.vue')
    }
]