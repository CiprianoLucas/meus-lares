import { type AxiosInstance } from 'axios';

interface LoginResponse {
    token: string;
    user: {
        id: number;
        username: string;
        role: string;
    };
}

interface LoginRequest {
    email: string;
    password: string;
}

interface CustomAxiosInstance extends AxiosInstance {
    login(form: LoginRequest): Promise<LoginResponse>;
}

export type { LoginResponse, LoginRequest, CustomAxiosInstance}