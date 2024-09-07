import type { RouteRecordRaw } from 'vue-router'
import {routes as auth} from '@/modules/auth'
import {routes as home} from '@/modules/home'
import {routes as example} from '@/modules/example'
import {routes as user} from '@/modules/user'
import {routes as places} from '@/modules/places'
import {routes as requests} from '@/modules/requests'

const routes: Array<RouteRecordRaw> = [
    //add the routes here
    ...auth,
    ...home,
    ...example,
    ...user,
    ...places,
    ...requests,
]
export {routes}