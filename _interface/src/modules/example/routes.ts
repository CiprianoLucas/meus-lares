export default [
    {
        path: '/example', //don't forget insert in router folder
        name: 'example', 
        component: () => import(/* webpacjChunkName: "example" */ './pages/ExampleExample.vue')
    }
]