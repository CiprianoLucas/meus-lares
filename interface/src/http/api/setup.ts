import axios from 'axios'
import { popup } from '@/components/PopUps'
import type { CustomAxiosInstance } from './interfaces'
import { userStore } from '@/modules/user/stores'

const api: CustomAxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true
}) as CustomAxiosInstance

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config

        if (
            error.response &&
            error.response.status === 403 &&
            originalRequest &&
            !originalRequest._retry
        ) {
            originalRequest._retry = true
            try {
                getCsrf()
                return api(originalRequest)
            } catch (err) {
                return Promise.reject(err)
            }
        }
        return Promise.reject(error)
    }
)

function getCsrf() {
    api.get('/user/info/').then(({ data }) => {
        api.defaults.headers.common['X-CSRFToken'] = data.csrftoken
        try {
            const user = userStore()
            if (user.id != data.id) {
                user.id = ''
                user.nick = ''
            } else {
                user.nick = data.nick
            }
        } catch {}
    })
}
getCsrf()

export default api
//DON'T CHANGE THIS FILE
