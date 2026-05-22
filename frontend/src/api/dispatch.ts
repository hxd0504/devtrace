import api from './index'
import type { AITag, AITagUpdate, DispatchRequest, DispatchResponse, DispatchRecord } from '@/types/dispatch'

export const dispatchApi = {
  dispatch(data: DispatchRequest): Promise<DispatchResponse> {
    return api.post('/dispatch', data)
  },
  getRecords(taskId?: number): Promise<DispatchRecord[]> {
    return api.get('/dispatch/records', { params: taskId ? { task_id: taskId } : {} })
  },
  getAITags(workspaceId?: number): Promise<AITag[]> {
    return api.get('/ai-tags', { params: workspaceId ? { workspace_id: workspaceId } : {} })
  },
  updateAITag(aiTool: string, data: AITagUpdate): Promise<AITag> {
    return api.put(`/ai-tags/${aiTool}`, data)
  },
}
