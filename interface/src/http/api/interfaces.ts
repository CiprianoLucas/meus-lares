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
    getCashed<T>(
        path: string, 
        force?: boolean, 
        time?: number
    ) : Promise<T>;
}

export type { LoginResponse, LoginRequest, CustomAxiosInstance}