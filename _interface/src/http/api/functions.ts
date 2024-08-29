import type { LoginResponse, LoginRequest} from './interfaces'
import { type AxiosResponse } from 'axios'
import Cookies from 'js-cookie'
import api from './setup'

api.login = async function(form: LoginRequest): Promise<LoginResponse> {
    try {
		if(localStorage.getItem('username')){
			await api.logout()
		}

		const response: AxiosResponse<LoginResponse> = await this.post('/user/login/', {
			username: form.username,
			password: form.password,
		});

		localStorage.setItem('username', response.data.username)
		if (response.data.isResident){
			localStorage.setItem('isResident', 'true')
		} else {
			localStorage.removeItem('isResident')
		}
		if (response.data.isUnion){
			localStorage.setItem('isUnion', 'true')
		} else {
			localStorage.removeItem('isUnion')
		}
		window.location.href = '/';
      	return response.data
    } catch (error) {
		console.error('Login failed:', error)
		throw error
    }
}

api.logout = async function() {
    try {
		await this.get('/user/logout/', {withCredentials: true})
		localStorage.clear()
		sessionStorage.clear()
		Cookies.remove('sessionid')
    } catch (error) {
		console.error('Logout failed:', error)
		throw error
    }
}

export default api