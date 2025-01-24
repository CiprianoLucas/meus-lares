import type { RouteRecordRaw } from 'vue-router'
import { routes as auth } from '@/modules/auth'
import { routes as home } from '@/modules/home'
import { routes as user } from '@/modules/user'
import { routes as places } from '@/modules/places'

const routes: Array<RouteRecordRaw> = [
    //add the routes here
    ...auth,
    ...home,
    ...user,
    ...places
]
export { routes }
