import { useRoute, type RouteLocationRaw } from 'vue-router'
import { popup, resumeErrors } from '@/components/PopUps'
import { api } from '@/http'
import { ref, onMounted } from 'vue'
import router from '@/router'

const app = {
    api: api,
    ref: ref,
    routeParam: (param: string) => useRoute().params[param],
    redirect: (param: RouteLocationRaw) => {
        router.push(param)
    },
    onMounted: onMounted,
    popup: popup,
    resumeErrors: resumeErrors,
}
export default app