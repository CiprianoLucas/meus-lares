import axios from 'axios';
import type { CustomAxiosInstance} from './interfaces'
import Cookies from 'js-cookie';

const api: CustomAxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL
}) as CustomAxiosInstance;

api.defaults.withCredentials = true
const csrftoken = Cookies.get('csrftoken')

if (csrftoken == undefined){
    api.get('/csrf/').then(({data})=>{
        api.defaults.headers.common['X-CSRFToken'] = data.csrfToken
    })
    .catch(() => {

    })
}
export default api
//DON'T CHANGE THIS FILE