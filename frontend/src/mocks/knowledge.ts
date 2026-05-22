import type { ThoughtChain } from '@/types/knowledge'

const mockThoughtChains: ThoughtChain[] = [
  {
    id: 1,
    workspace_id: 1,
    problem: 'Docker 镜像拉取失败',
    thought_chain: [
      '检查网络连接 - ping docker.io 失败',
      '检查镜像源配置 - 使用默认源',
      '发现是代理问题 - 服务器未配置代理',
      '配置国内镜像源 - 修改 daemon.json',
      '测试拉取成功 - docker pull nginx 成功',
    ],
    tags: ['Docker', '网络', '代理'],
    source: 'auto_extract',
    related_issue_ids: [1, 3],
    created_at: '2026-05-22T09:30:00Z',
    updated_at: '2026-05-22T09:30:00Z',
  },
  {
    id: 2,
    workspace_id: 1,
    problem: 'JWT Token 过期处理',
    thought_chain: [
      '用户反馈频繁掉线',
      '检查 token 过期时间设置 - 30分钟',
      '分析 refresh token 机制 - 未实现',
      '实现 token 自动刷新逻辑',
      '添加 axios 拦截器处理 401',
    ],
    tags: ['JWT', '认证', '前端'],
    source: 'auto_extract',
    related_issue_ids: [2],
    created_at: '2026-05-22T11:00:00Z',
    updated_at: '2026-05-22T11:00:00Z',
  },
  {
    id: 3,
    workspace_id: 1,
    problem: '数据库连接池耗尽',
    thought_chain: [
      '应用日志出现 connection timeout',
      '检查数据库连接数 - 达到上限',
      '分析慢查询日志 - 发现未加索引的查询',
      '添加缺失索引',
      '调整连接池大小为 20',
    ],
    tags: ['数据库', '性能', 'PostgreSQL'],
    source: 'manual',
    related_issue_ids: [],
    created_at: '2026-05-22T14:00:00Z',
    updated_at: '2026-05-22T14:00:00Z',
  },
]

let nextId = 4

export const mockKnowledgeApi = {
  list(workspaceId: number): Promise<ThoughtChain[]> {
    return Promise.resolve(mockThoughtChains.filter((tc) => tc.workspace_id === workspaceId))
  },
  create(data: { workspace_id: number; problem: string; thought_chain: string[]; tags?: string[]; source?: string; related_issue_ids?: number[] }): Promise<ThoughtChain> {
    const tc: ThoughtChain = {
      id: nextId++,
      workspace_id: data.workspace_id,
      problem: data.problem,
      thought_chain: data.thought_chain,
      tags: data.tags || [],
      source: (data.source as ThoughtChain['source']) || 'manual',
      related_issue_ids: data.related_issue_ids || [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    mockThoughtChains.push(tc)
    return Promise.resolve(tc)
  },
  search(workspaceId: number, query: string): Promise<ThoughtChain[]> {
    const results = mockThoughtChains.filter(
      (tc) =>
        tc.workspace_id === workspaceId &&
        (tc.problem.includes(query) || tc.tags.some((t) => t.includes(query)) || tc.thought_chain.some((s) => s.includes(query))),
    )
    return Promise.resolve(results)
  },
  extract(conversationId: number): Promise<ThoughtChain[]> {
    // 模拟从对话中提取思维链
    const tc: ThoughtChain = {
      id: nextId++,
      workspace_id: 1,
      problem: `从对话 #${conversationId} 自动提取的问题`,
      thought_chain: ['分析对话内容', '识别关键问题', '提取解决步骤', '保存到知识库'],
      tags: ['自动提取'],
      source: 'auto_extract',
      related_issue_ids: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    mockThoughtChains.push(tc)
    return Promise.resolve([tc])
  },
}
