import api from './index'
import type { LoginRequest, TokenResponse, User } from '@/types/auth'

export const authApi = {
  login(data: LoginRequest): Promise<TokenResponse> {
    return api.post('/auth/login', data)
  },
  getMe(): Promise<User> {
    return api.get('/auth/me')
  },
}
