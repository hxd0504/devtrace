import type { ExecutorType, RelatedFile, ActivityLogEntry } from './issue'

export type TaskStatus = 'todo' | 'doing' | 'done'
export type RiskLevel = 'low' | 'medium' | 'high'

export interface Task {
  id: number
  issue_id: number
  title: string
  description: string | null
  status: TaskStatus
  owner_name: string | null
  executor_name: string | null
  executor_type: ExecutorType | null
  executor_note: string | null
  related_files: RelatedFile[]
  evidence_source: string | null
  evidence_summary: string | null
  acceptance_criteria: string | null
  risk_level: RiskLevel | null
  activity_log: ActivityLogEntry[]
  version: number
  created_at: string
  updated_at: string
}

export interface TaskCreate {
  title: string
  description?: string
  owner_name?: string
  executor_name?: string
  executor_type?: ExecutorType
  executor_note?: string
  related_files?: RelatedFile[]
  evidence_source?: string
  evidence_summary?: string
  acceptance_criteria?: string
  risk_level?: RiskLevel
  tags?: string[]
}

export interface TaskUpdate {
  title?: string
  description?: string
  owner_name?: string
  executor_name?: string
  executor_type?: ExecutorType
  executor_note?: string
  related_files?: RelatedFile[]
  evidence_source?: string
  evidence_summary?: string
  acceptance_criteria?: string
  risk_level?: RiskLevel
  version: number
}

export interface TaskStatusChangeRequest {
  status: TaskStatus
  version: number
  details?: string
}

// V1.1 AI 智能创建
export interface TaskDraftRequest {
  intent: string
  workspace_id: number
  issue_id: number
  context?: {
    recent_messages?: string[]
    related_files?: RelatedFile[]
    evidence?: string[]
  }
}

export interface TaskDraftResponse {
  title: string
  description: string
  executor_type: ExecutorType
  executor_name: string
  owner_name: string
  evidence_summary: string
  acceptance_criteria: string
  risk_level: RiskLevel
  tags: string[]
}

export interface ExecutorRecommend {
  name: string
  type: ExecutorType
  score: number
}
