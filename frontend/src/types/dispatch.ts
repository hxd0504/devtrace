export interface AITag {
  id: number
  ai_tool: string
  workspace_id: number | null
  tags: Record<string, unknown>
  stats: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface AITagUpdate {
  tags?: Record<string, unknown>
  stats?: Record<string, unknown>
}

export interface DispatchRequest {
  task_id: number
  task_type?: string
  preferred_ai?: string
}

export interface DispatchResponse {
  id: number
  task_id: number
  ai_tool: string
  dispatch_reason: string | null
  risk_level: string | null
  execution_prompt: string | null
  success: boolean | null
  created_at: string
}

export interface DispatchRecord extends DispatchResponse {
  execution_result: string | null
  duration_seconds: number | null
}
