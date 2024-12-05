import type { LoginResponse, LoginRequest } from './interfaces'
import { type AxiosResponse } from 'axios'
import api from './setup'

api.login = async function (form) {
    try {
        if (localStorage.getItem('username')) {
            await api.logout()
        }

        const response: AxiosResponse<LoginResponse> = await this.post('/user/login/', {
            username: form.username,
            password: form.password
        })

        localStorage.setItem('username', response.data.username)
        if (response.data.isResident) {
            localStorage.setItem('isResident', 'true')
        } else {
            localStorage.removeItem('isResident')
        }
        if (response.data.isUnion) {
            localStorage.setItem('isUnion', 'true')
        } else {
            localStorage.removeItem('isUnion')
        }
        window.location.href = '/'
        return response.data
    } catch (error) {
        throw error
    }
}

api.logout = async function () {
    localStorage.clear()
    sessionStorage.clear()
    try {
        await this.get('/user/logout/', { withCredentials: true })
    } catch (error) {
        throw error
    }
}

api.getCashed = async function (path, force?, time?) {
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
                return obj.response
            }
        }
        const response = (await this.get(path)).data
        const session = {
            response: response,
            createAt: timestampAtual,
            expirate: actualTime * 1000
        }

        sessionStorage.setItem(path, JSON.stringify(session))

        return response
    } catch (error) {
        throw error
    }
}

export default api
