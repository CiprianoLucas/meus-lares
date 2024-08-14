import type { RouteRecordRaw } from 'vue-router'
import {routes as auth} from '@/modules/auth'
import {routes as home} from '@/modules/home'
import {routes as example} from '@/modules/example'
import {routes as chat} from '@/modules/chat'

const routes: Array<RouteRecordRaw> = [
    //add the routes here
    ...auth,
    ...home,
    ...example,
    ...chat
]
export {routes}