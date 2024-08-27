import { type AxiosInstance } from 'axios';

interface LoginResponse {
    username: string;
    isResident: boolean;
    isUnion: boolean;
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