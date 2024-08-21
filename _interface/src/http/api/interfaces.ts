import { type AxiosInstance } from 'axios';

interface LoginResponse {
    username: string;
}

interface LoginRequest {
    username: string;
    password: string;
}

interface CustomAxiosInstance extends AxiosInstance {
    login(form: LoginRequest): Promise<LoginResponse>,
    logout() : Promise<void>;
}

export type { LoginResponse, LoginRequest, CustomAxiosInstance}