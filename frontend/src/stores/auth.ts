import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'
import type { User } from '@/types/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') as string | null,
    user: null as User | null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(username: string, password: string) {
      const res = await authApi.login({ username, password })
      this.token = res.access_token
      localStorage.setItem('token', res.access_token)
      await this.fetchMe()
    },
    async fetchMe() {
      this.user = await authApi.getMe()
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
  },
})
