import axios from 'axios';
import type { CustomAxiosInstance} from './interfaces'
import Cookies from 'js-cookie';

const api: CustomAxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true
}) as CustomAxiosInstance;

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;
        
        if (error.response && error.response.status === 403 && originalRequest && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                getUserAndCsrf()
                return api(originalRequest);
            } catch (err) {
                return Promise.reject(err);
            }
        }
        return Promise.reject(error);
    }
  );

function getUserAndCsrf(){
    api.get('/user/info/').then(({data})=>{
        api.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
        if(data.username != "Anonimous"){
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
}
getUserAndCsrf()

export default api
//DON'T CHANGE THIS FILE