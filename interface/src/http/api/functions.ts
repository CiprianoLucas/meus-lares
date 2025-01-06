import type { LoginResponse, LoginRequest } from './interfaces'
import { type AxiosResponse } from 'axios'
import api from './setup'
import router from '@/router'
import { userStore } from '@/modules/user/stores'

api.login = async function (form) {
    try {
        const user = userStore()
        user.username = ''
        const response: AxiosResponse<LoginResponse> = await this.post('/user/login/', {
            username: form.username,
            password: form.password
        })
        user.username = response.data.username
        user.roles = response.data.roles
        if (!user.roles.includes(user.role)) {
            user.role = ''
        }
        router.replace('/')
        return response.data
    } catch (error) {
        throw error
    }
}

api.logout = async function () {
    const user = userStore()
    user.username = ''
    this.get('/user/logout/', { withCredentials: true })
    router.replace('/login')
}

api.getListCashed = async function (path, force?, time?) {
    try {
        const actualForce = force !== undefined ? force : false
        const actualTime = time !== undefined ? time : 300
        const timestampAtual = Date.now()
        const sessionCash = sessionStorage.getItem(path)

        if (sessionCash) {
            const obj = JSON.parse(sessionCash)

            if (
                obj.createAt + 30000 > timestampAtual ||
                (obj.createAt + 30000 < timestampAtual && !actualForce) ||
                (obj.createAt + obj.expirate > timestampAtual && actualForce)
            ) {
                const response = obj.response
                const result = response.results
                const count = response.count
                const next = response.next
                const previous = response.previous
                return { result, count, next, previous }
            }
        }
        const response = (await this.get(path)).data

        const session = {
            response: response,
            createAt: timestampAtual,
            expirate: actualTime * 1000
        }

        sessionStorage.setItem(path, JSON.stringify(session))

        const result = response.results
        const count = response.count
        const next = response.next
        const previous = response.previous
        return { result, count, next, previous }
    } catch (error) {
        throw error
    }
}

export default api
