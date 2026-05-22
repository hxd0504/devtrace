import type { LoginRequest, TokenResponse, User } from '@/types/auth'

const mockUser: User = { id: 1, username: 'admin' }

export const mockAuthApi = {
  login(_data: LoginRequest): Promise<TokenResponse> {
    return Promise.resolve({ access_token: 'mock-token-xxx', token_type: 'bearer' })
  },
  getMe(): Promise<User> {
    return Promise.resolve(mockUser)
  },
}
