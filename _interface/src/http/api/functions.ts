import type { LoginResponse, LoginRequest} from './interfaces'
import { type AxiosResponse } from 'axios';
import api from './setup'

api.login = async function(form: LoginRequest): Promise<LoginResponse> {
    try {
      const response: AxiosResponse<LoginResponse> = await this.post('/auth/login/', {
        email: form.email,
        password: form.password,
      });
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  };  

export default api