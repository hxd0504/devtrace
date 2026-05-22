import api from './index'
import type { Conversation, ConversationCreate, Message, MessageCreate } from '@/types/conversation'

export const conversationApi = {
  list(workspaceId: number): Promise<Conversation[]> {
    return api.get('/conversations', { params: { workspace_id: workspaceId } })
  },
  get(id: number): Promise<Conversation> {
    return api.get(`/conversations/${id}`)
  },
  create(data: ConversationCreate): Promise<Conversation> {
    return api.post('/conversations', data)
  },
  getMessages(conversationId: number): Promise<Message[]> {
    return api.get(`/conversations/${conversationId}/messages`)
  },
  sendMessage(conversationId: number, data: MessageCreate): Promise<Message> {
    return api.post(`/conversations/${conversationId}/messages`, data)
  },
}
