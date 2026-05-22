export interface ThoughtChain {
  id: number
  workspace_id: number
  problem: string
  thought_chain: string[]
  tags: string[]
  source: 'auto_extract' | 'manual'
  related_issue_ids: number[]
  created_at: string
  updated_at: string
}

export interface ThoughtChainCreate {
  workspace_id: number
  problem: string
  thought_chain: string[]
  tags?: string[]
  source?: 'auto_extract' | 'manual'
  related_issue_ids?: number[]
}
