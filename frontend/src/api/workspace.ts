import api from './index'
import type { Workspace, WorkspaceCreate } from '@/types/workspace'

export const workspaceApi = {
  list(): Promise<{ items: Workspace[] }> {
    return api.get('/workspaces')
  },
  get(id: number): Promise<Workspace> {
    return api.get(`/workspaces/${id}`)
  },
  create(data: WorkspaceCreate): Promise<Workspace> {
    return api.post('/workspaces', data)
  },
}
