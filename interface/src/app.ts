import { useRouter, useRoute } from 'vue-router';
import { popup } from '@/components/PopUps';
import { api } from '@/http'
import { ref, onMounted } from 'vue'

const app = {
    api: api,
    ref: ref,
    useRoute: useRoute,
    useRouter: useRouter,
    onMounted: onMounted,
    popup: popup,
};
export default app