import type { LoginResponse, LoginRequest} from './interfaces'
import { type AxiosResponse } from 'axios';
import Cookies from 'js-cookie';
import api from './setup'

api.login = async function(form: LoginRequest): Promise<LoginResponse> {
    try {
		const response: AxiosResponse<LoginResponse> = await this.post('/user/login/', {
			username: form.username,
			password: form.password,
		});
		localStorage.setItem('username', response.data.username);
      	return response.data
    } catch (error) {
		console.error('Login failed:', error);
		throw error
    }
}

api.logout = async function() {
    try {
		await this.post('/user/logout/', {}, {withCredentials: true});
		localStorage.clear()
		Cookies.remove('sessionid');
    } catch (error) {
		console.error('Login failed:', error);
		throw error
    }
}

export default api