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
  ai_tool?: string
  reason?: string
}

export interface DispatchResponse {
  recommended_tool: string
  reason: string
  risk_level: string
  execution_prompt: string
  alternatives: { tool: string; reason: string }[]
}

export interface DispatchRecord {
  id: number
  task_id: number
  ai_tool: string
  dispatch_reason: string | null
  risk_level: string | null
  execution_prompt: string | null
  execution_result: string | null
  duration_seconds: number | null
  success: boolean | null
  created_at: string
}
