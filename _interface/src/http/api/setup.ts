import axios from 'axios';
import type { CustomAxiosInstance} from './interfaces'
import Cookies from 'js-cookie';

const api: CustomAxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL
}) as CustomAxiosInstance;

api.defaults.withCredentials = true

api.get('/user/info/').then(({data})=>{
    console.log(data)
    const csrfToken = Cookies.get('csrftoken');
        if (csrfToken) {
            api.defaults.headers.common['X-CSRFToken'] = csrfToken;
        }
    if(data.username =! "Anonimous"){
        localStorage.setItem("username", data.username)
        if (data.isResident){
            localStorage.setItem('isResident', 'true')
        } else {
            localStorage.removeItem('isResident')
        }
        if (data.isUnion){
            localStorage.setItem('isUnion', 'true')
        } else {
            localStorage.removeItem('isUnion')
        }
    } else {
        localStorage.clear()
    }
})
export default api
//DON'T CHANGE THIS FILE