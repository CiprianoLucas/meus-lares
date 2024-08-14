import axios from 'axios';
import type { CustomAxiosInstance} from './interfaces'

const api: CustomAxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL
}) as CustomAxiosInstance;

api.get('/csrf/', { withCredentials: true }).then(({data})=>{
    api.defaults.headers.common['X-CSRFToken'] = data.csrfToken
    api.defaults.withCredentials = true
})
.catch(() => {

})

export default api
//DON'T CHANGE THIS FILE