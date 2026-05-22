import api from './index'
import type { Issue, IssueCreate, IssueUpdate, StatusChangeRequest, ArchiveRequest } from '@/types/issue'

export const issueApi = {
  list(workspaceId: number, status?: string): Promise<Issue[]> {
    return api.get(`/workspaces/${workspaceId}/issues`, { params: status ? { status } : {} })
  },
  get(workspaceId: number, issueId: number): Promise<Issue> {
    return api.get(`/workspaces/${workspaceId}/issues/${issueId}`)
  },
  create(workspaceId: number, data: IssueCreate): Promise<Issue> {
    return api.post(`/workspaces/${workspaceId}/issues`, data)
  },
  update(workspaceId: number, issueId: number, data: IssueUpdate): Promise<Issue> {
    return api.put(`/workspaces/${workspaceId}/issues/${issueId}`, data)
  },
  changeStatus(workspaceId: number, issueId: number, data: StatusChangeRequest): Promise<Issue> {
    return api.put(`/workspaces/${workspaceId}/issues/${issueId}/status`, data)
  },
  archive(workspaceId: number, issueId: number, data: ArchiveRequest): Promise<Issue> {
    return api.post(`/workspaces/${workspaceId}/issues/${issueId}/archive`, data)
  },
  addNote(workspaceId: number, issueId: number, details: string): Promise<Issue> {
    return api.post(`/workspaces/${workspaceId}/issues/${issueId}/notes`, { details })
  },
}
