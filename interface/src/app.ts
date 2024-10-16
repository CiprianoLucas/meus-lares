import { useRouter, useRoute } from 'vue-router';
import { popup, resumeErrors } from '@/components/PopUps';
import { api } from '@/http'
import { ref, onMounted } from 'vue'

const app = {
    api: api,
    ref: ref,
    useRoute: useRoute,
    useRouter: useRouter,
    onMounted: onMounted,
    popup: popup,
    resumeErrors: resumeErrors,
};
export default app