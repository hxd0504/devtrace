import type { AITag, DispatchResponse, DispatchRecord } from '@/types/dispatch'

const mockAITags: AITag[] = [
  {
    id: 1,
    ai_tool: 'Claude Code',
    workspace_id: 1,
    tags: { specialty: ['backend', 'frontend', 'docs'] },
    stats: { speed: 0.8, quality: 0.7, stability: 0.9 },
    created_at: '2026-05-22T00:00:00Z',
    updated_at: '2026-05-22T00:00:00Z',
  },
  {
    id: 2,
    ai_tool: 'Codex',
    workspace_id: 1,
    tags: { specialty: ['test', 'debug'] },
    stats: { speed: 0.6, quality: 0.8, stability: 0.7 },
    created_at: '2026-05-22T00:00:00Z',
    updated_at: '2026-05-22T00:00:00Z',
  },
  {
    id: 3,
    ai_tool: 'GPT',
    workspace_id: 1,
    tags: { specialty: ['design', 'docs'] },
    stats: { speed: 0.7, quality: 0.75, stability: 0.85 },
    created_at: '2026-05-22T00:00:00Z',
    updated_at: '2026-05-22T00:00:00Z',
  },
]

const mockRecords: DispatchRecord[] = [
  {
    id: 1,
    task_id: 1,
    ai_tool: 'Claude Code',
    dispatch_reason: '代码生成任务，推荐使用 Claude Code',
    risk_level: 'low',
    execution_prompt: '请实现用户登录功能，包含 JWT 认证',
    execution_result: '已完成 Login.vue 和 auth store 的实现',
    duration_seconds: 45,
    success: true,
    created_at: '2026-05-22T10:01:00Z',
  },
]

export const mockDispatchApi = {
  dispatch(data: { task_id: number; ai_tool?: string }): Promise<DispatchResponse> {
    return Promise.resolve({
      recommended_tool: data.ai_tool || 'Claude Code',
      reason: '基于任务类型分析，推荐使用 Claude Code 执行代码生成任务',
      risk_level: 'low',
      execution_prompt: `请执行以下任务（Task #${data.task_id}）：\n根据上下文信息完成代码实现`,
      alternatives: [
        { tool: 'Codex', reason: '备选方案，适合测试代码生成' },
        { tool: 'GPT', reason: '适合文档和方案设计' },
      ],
    })
  },
  getRecords(taskId?: number): Promise<DispatchRecord[]> {
    if (taskId) return Promise.resolve(mockRecords.filter((r) => r.task_id === taskId))
    return Promise.resolve(mockRecords)
  },
  getAITags(workspaceId?: number): Promise<AITag[]> {
    if (workspaceId) return Promise.resolve(mockAITags.filter((t) => t.workspace_id === workspaceId))
    return Promise.resolve(mockAITags)
  },
  updateAITag(aiTool: string, data: { tags?: Record<string, unknown>; stats?: Record<string, unknown> }): Promise<AITag> {
    const tag = mockAITags.find((t) => t.ai_tool === aiTool)
    if (!tag) return Promise.reject(new Error('AI Tag not found'))
    if (data.tags) tag.tags = { ...tag.tags, ...data.tags }
    if (data.stats) tag.stats = { ...tag.stats, ...data.stats }
    tag.updated_at = new Date().toISOString()
    return Promise.resolve(tag)
  },
}
