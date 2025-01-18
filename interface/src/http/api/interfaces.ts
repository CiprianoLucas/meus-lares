import { type AxiosInstance } from 'axios'
import type { Role } from '@/modules/user/interfaces'

interface LoginResponse {
    email: string
    role: Role
    roles: Role[]
}

interface LoginRequest {
    email: string
    password: string
}

interface CustomAxiosInstance extends AxiosInstance {
    login(form: LoginRequest): Promise<LoginResponse>
    logout(): Promise<void>
    getListCashed<T>(path: string, force?: boolean, time?: number): Promise<{ result: T; count: number; next: string | null; previous: string | null }>
    removeListCash(path: string): Promise<void>
    clearCash(): Promise<void>
}

export type { LoginResponse, LoginRequest, CustomAxiosInstance }
