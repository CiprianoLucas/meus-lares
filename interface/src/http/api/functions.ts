import type { LoginResponse, LoginRequest } from './interfaces'
import { type AxiosResponse } from 'axios'
import api from './setup'
import router from '@/router'
import { userStore } from '@/modules/user/stores'
import { apiListStore } from './stores'

api.login = async function (form) {
    try {
        const user = userStore()
        const cash = apiListStore()
        user.email = ''
        const response: AxiosResponse<LoginResponse> = await this.post('/user/login/', {
            email: form.email,
            password: form.password
        })
        user.email = response.data.email
        user.roles = response.data.roles
        if (!user.roles.includes(user.role)) {
            cash.clear()
            user.role = ''
        }
        return response.data
    } catch (error) {
        throw error
    }
}
api.logout = async function () {
    const user = userStore()
    user.email = ''
    this.get('/user/logout/', { withCredentials: true })
    router.push('/login')
}

api.clearCash = async function () {
    const cash = apiListStore()
    cash.clear()
}

api.removeListCash = async function (path) {
    const cash = apiListStore()
    cash.remove(path)
}

api.getListCashed = async function (path, force?, time?) {
    try {
        const actualForce = force !== undefined ? force : false
        const actualTime = time !== undefined ? time : 300
        const timestampAtual = Date.now()
        const cash = apiListStore()
        const obj = cash.getResult(path)

        if (obj) {

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

        cash.setResult(path, session)

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
