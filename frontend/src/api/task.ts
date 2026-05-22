import api from './index'
import type { Task, TaskCreate, TaskUpdate, TaskStatusChangeRequest, TaskDraftRequest, TaskDraftResponse, ExecutorRecommend } from '@/types/task'

export const taskApi = {
  list(workspaceId: number, issueId: number): Promise<Task[]> {
    return api.get(`/workspaces/${workspaceId}/issues/${issueId}/tasks`)
  },
  create(workspaceId: number, issueId: number, data: TaskCreate): Promise<Task> {
    return api.post(`/workspaces/${workspaceId}/issues/${issueId}/tasks`, data)
  },
  update(workspaceId: number, issueId: number, taskId: number, data: TaskUpdate): Promise<Task> {
    return api.put(`/workspaces/${workspaceId}/issues/${issueId}/tasks/${taskId}`, data)
  },
  changeStatus(workspaceId: number, issueId: number, taskId: number, data: TaskStatusChangeRequest): Promise<Task> {
    return api.put(`/workspaces/${workspaceId}/issues/${issueId}/tasks/${taskId}/status`, data)
  },
  addNote(workspaceId: number, issueId: number, taskId: number, details: string): Promise<Task> {
    return api.post(`/workspaces/${workspaceId}/issues/${issueId}/tasks/${taskId}/notes`, { details })
  },
  // V1.1 AI 智能创建
  generateDraft(data: TaskDraftRequest): Promise<TaskDraftResponse> {
    return api.post('/tasks/draft', data)
  },
  getExecutors(workspaceId: number): Promise<ExecutorRecommend[]> {
    return api.get('/executors', { params: { workspace_id: workspaceId } })
  },
}
