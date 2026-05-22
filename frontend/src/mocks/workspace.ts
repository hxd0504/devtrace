import type { Workspace, WorkspaceCreate, WorkspaceListResponse } from '@/types/workspace'

const mockWorkspaces: Workspace[] = [
  { id: 1, name: 'DevTrace 自身开发项目', description: 'DevTrace 平台的开发和维护', owner_id: 1, created_at: '2026-05-21T10:00:00Z' },
  { id: 2, name: 'Docker 环境问题', description: 'Docker 相关的环境配置问题', owner_id: 1, created_at: '2026-05-20T15:30:00Z' },
]

export const mockWorkspaceApi = {
  list(): Promise<WorkspaceListResponse> {
    return Promise.resolve({ items: mockWorkspaces })
  },
  get(id: number): Promise<Workspace> {
    const w = mockWorkspaces.find((x) => x.id === id)
    return w ? Promise.resolve(w) : Promise.reject(new Error('Not found'))
  },
  create(data: WorkspaceCreate): Promise<Workspace> {
    const item: Workspace = { id: mockWorkspaces.length + 1, name: data.name, description: data.description || null, owner_id: 1, created_at: new Date().toISOString() }
    mockWorkspaces.push(item)
    return Promise.resolve(item)
  },
}
