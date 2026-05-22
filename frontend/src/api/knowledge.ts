import api from './index'
import type { ThoughtChain, ThoughtChainCreate } from '@/types/knowledge'

export const knowledgeApi = {
  list(workspaceId: number): Promise<ThoughtChain[]> {
    return api.get('/thought-chains', { params: { workspace_id: workspaceId } })
  },
  create(data: ThoughtChainCreate): Promise<ThoughtChain> {
    return api.post('/thought-chains', data)
  },
  search(workspaceId: number, query: string): Promise<ThoughtChain[]> {
    return api.get('/thought-chains/search', { params: { workspace_id: workspaceId, q: query } })
  },
  extract(conversationId: number): Promise<ThoughtChain[]> {
    return api.post('/knowledge/extract', { conversation_id: conversationId })
  },
}
