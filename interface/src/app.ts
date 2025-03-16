import { useRoute } from 'vue-router'
import { popup, resumeErrors } from '@/components/PopUps'
import { api } from '@/http'
import { ref, onMounted, watch, onBeforeMount } from 'vue'
import { loagingPageStore } from './components/template/Loading/stores'
import { delay } from './components/handlers'

const app = {
    api: api,
    ref: ref,
    routeQuery: (param: string) => useRoute().query[param],
    routeParam: (param: string) => useRoute().params[param],
    loading: (show: boolean, message: string = 'Carregando...') =>
        loagingPageStore().loading(show, message),
    onMounted: onMounted,
    onBeforeMount: onBeforeMount,
    popup: popup,
    resumeErrors: resumeErrors,
    watch: watch,
    delay: delay
}
export default app
