export default [
    {
        path: '/chat', 
        name: 'listChats', 
        component: () => import(/* webpacjChunkName: "List chats" */ './pages/ListChats.vue')
    },
    {
        path: '/chat/:userId',
        name: 'userChat', 
        component: () => import(/* webpacjChunkName: "User chat" */ './pages/UserChat.vue')
    }
]