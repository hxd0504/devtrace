export interface Workspace {
  id: number
  name: string
  description: string | null
  owner_id: number
  created_at: string
}

export interface WorkspaceCreate {
  name: string
  description?: string
}

export interface WorkspaceListResponse {
  items: Workspace[]
}
