import api from './index'
import type { Conversation } from '@/types/conversation'

export const importApi = {
  importChatGPT(data: { url?: string; content: string }): Promise<Conversation> {
    return api.post('/import/chatgpt', data)
  },
  importManual(data: { title: string; content: string; workspace_id: number }): Promise<Conversation> {
    return api.post('/import/manual', data)
  },
}
