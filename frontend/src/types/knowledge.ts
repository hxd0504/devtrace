export interface ThoughtStep {
  step?: number
  content: string
  role?: string
}

export interface ThoughtChain {
  id: number
  workspace_id: number
  problem: string
  thought_chain: ThoughtStep[]
  tags: string[]
  source: 'auto_extract' | 'manual'
  related_issue_ids: number[]
  created_at: string
  updated_at: string
}

export interface ThoughtChainCreate {
  workspace_id: number
  problem: string
  thought_chain: ThoughtStep[]
  tags?: string[]
  source?: 'auto_extract' | 'manual'
  related_issue_ids?: number[]
}
