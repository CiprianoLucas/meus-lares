import { useRoute, useRouter, type RouteLocationRaw } from 'vue-router'
import { popup, resumeErrors } from '@/components/PopUps'
import { api } from '@/http'
import { ref, onMounted, watch, onBeforeMount } from 'vue'

const app = {
    api: api,
    ref: ref,
    routeQuery: (param: string) => useRoute().query[param],
    routeParam: (param: string) => useRoute().params[param],
    onMounted: onMounted,
    onBeforeMount: onBeforeMount,
    popup: popup,
    resumeErrors: resumeErrors,
    watch: watch
}
export default app
