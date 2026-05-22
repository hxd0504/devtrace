export type IssueStatus = 'open' | 'in_progress' | 'resolved' | 'archived'
export type ExecutorType = 'human' | 'ai_window' | 'role' | 'tool'

export interface RelatedFile {
  name: string
  path: string
  note: string
}

export interface ActivityLogEntry {
  timestamp: string
  user_id: number
  username: string
  action: string
  details?: string
  from_status?: string
  to_status?: string
}

export interface Issue {
  id: number
  workspace_id: number
  title: string
  description: string | null
  status: IssueStatus
  creator_id: number
  assignee_name: string | null
  executor_name: string | null
  executor_type: ExecutorType | null
  executor_note: string | null
  related_files: RelatedFile[]
  evidence_note: string | null
  root_cause: string | null
  failed_attempts: string | null
  final_solution: string | null
  reusable: boolean
  tags: string[]
  activity_log: ActivityLogEntry[]
  version: number
  created_at: string
  updated_at: string
}

export interface IssueCreate {
  title: string
  description?: string
  assignee_name?: string
  executor_name?: string
  executor_type?: ExecutorType
  executor_note?: string
  related_files?: RelatedFile[]
  evidence_note?: string
}

export interface IssueUpdate {
  title?: string
  description?: string
  assignee_name?: string
  executor_name?: string
  executor_type?: ExecutorType
  executor_note?: string
  related_files?: RelatedFile[]
  evidence_note?: string
  version: number
}

export interface StatusChangeRequest {
  status: IssueStatus
  version: number
  details?: string
}

export interface ArchiveRequest {
  root_cause: string
  failed_attempts: string
  final_solution: string
  reusable: boolean
  tags?: string[]
  version: number
}
