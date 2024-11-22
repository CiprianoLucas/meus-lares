import { useRoute, type RouteLocationRaw } from 'vue-router'
import { popup, resumeErrors } from '@/components/PopUps'
import { api } from '@/http'
import { ref, onMounted, watch } from 'vue'
import router from '@/router'

const app = {
    api: api,
    ref: ref,
    routeQuery: (param: string) => useRoute().query[param],
    routeParam: (param: string) => useRoute().params[param],
    redirect: (param: RouteLocationRaw) => {
        router.replace(param).then(()=>window.location.reload());
    },
    onMounted: onMounted,
    popup: popup,
    resumeErrors: resumeErrors,
    watch: watch,
}
export default app