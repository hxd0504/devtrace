import type { Issue, IssueCreate, IssueUpdate, StatusChangeRequest, ArchiveRequest } from '@/types/issue'

const mockIssues: Issue[] = [
  {
    id: 1, workspace_id: 1, title: '前端路由配置问题', description: 'Vue Router 配置后页面无法正常跳转', status: 'open', creator_id: 1,
    assignee_name: null, executor_name: 'Claude Code 窗口A', executor_type: 'ai_window', executor_note: null,
    related_files: [], evidence_note: null, root_cause: null, failed_attempts: null, final_solution: null,
    reusable: false, tags: [], activity_log: [], version: 1, created_at: '2026-05-21T10:00:00Z', updated_at: '2026-05-21T10:00:00Z',
  },
  {
    id: 2, workspace_id: 1, title: 'Docker 镜像拉取失败', description: '启动 vLLM 服务时 docker pull 超时', status: 'archived', creator_id: 1,
    assignee_name: 'admin', executor_name: 'Claude Code 窗口A', executor_type: 'ai_window', executor_note: '负责 Docker 环境配置',
    related_files: [], evidence_note: 'docker pull 超时', root_cause: 'VPN/镜像源配置异常', failed_attempts: '重启Docker、更换网络',
    final_solution: '配置国内镜像源', reusable: true, tags: ['Docker'], activity_log: [], version: 5, created_at: '2026-05-20T10:00:00Z', updated_at: '2026-05-21T09:00:00Z',
  },
]

export const mockIssueApi = {
  list(_workspaceId: number, _status?: string): Promise<Issue[]> {
    return Promise.resolve(mockIssues)
  },
  get(_workspaceId: number, issueId: number): Promise<Issue> {
    const i = mockIssues.find((x) => x.id === issueId)
    return i ? Promise.resolve(i) : Promise.reject(new Error('Not found'))
  },
  create(_workspaceId: number, data: IssueCreate): Promise<Issue> {
    const item: Issue = {
      id: mockIssues.length + 1, workspace_id: _workspaceId, title: data.title, description: data.description || null,
      status: 'open', creator_id: 1, assignee_name: data.assignee_name || null, executor_name: data.executor_name || null,
      executor_type: data.executor_type || null, executor_note: data.executor_note || null, related_files: data.related_files || [],
      evidence_note: data.evidence_note || null, root_cause: null, failed_attempts: null, final_solution: null,
      reusable: false, tags: [], activity_log: [], version: 1, created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    }
    mockIssues.push(item)
    return Promise.resolve(item)
  },
  update(_workspaceId: number, issueId: number, data: IssueUpdate): Promise<Issue> {
    const issue = mockIssues.find((x) => x.id === issueId)
    if (!issue) return Promise.reject(new Error('Not found'))
    if (issue.version !== data.version) return Promise.reject({ response: { status: 409, data: { detail: '版本冲突，请刷新后重试' } } })
    Object.assign(issue, { ...data, version: issue.version + 1, updated_at: new Date().toISOString() })
    return Promise.resolve(issue)
  },
  changeStatus(_workspaceId: number, issueId: number, data: StatusChangeRequest): Promise<Issue> {
    const issue = mockIssues.find((x) => x.id === issueId)
    if (!issue) return Promise.reject(new Error('Not found'))
    issue.status = data.status
    issue.version += 1
    issue.updated_at = new Date().toISOString()
    issue.activity_log.push({
      timestamp: new Date().toISOString(),
      user_id: 1,
      username: 'admin',
      action: 'status_change',
      from_status: issue.status,
      to_status: data.status,
      details: data.details,
    })
    return Promise.resolve(issue)
  },
  archive(_workspaceId: number, issueId: number, data: ArchiveRequest): Promise<Issue> {
    const issue = mockIssues.find((x) => x.id === issueId)
    if (!issue) return Promise.reject(new Error('Not found'))
    issue.status = 'archived'
    issue.root_cause = data.root_cause
    issue.failed_attempts = data.failed_attempts
    issue.final_solution = data.final_solution
    issue.reusable = data.reusable
    issue.tags = data.tags || []
    issue.version += 1
    issue.updated_at = new Date().toISOString()
    issue.activity_log.push({
      timestamp: new Date().toISOString(),
      user_id: 1,
      username: 'admin',
      action: 'archived',
      details: '问题已归档',
    })
    return Promise.resolve(issue)
  },
  addNote(_workspaceId: number, issueId: number, details: string): Promise<Issue> {
    const issue = mockIssues.find((x) => x.id === issueId)
    if (!issue) return Promise.reject(new Error('Not found'))
    issue.activity_log.push({
      timestamp: new Date().toISOString(),
      user_id: 1,
      username: 'admin',
      action: 'note',
      details,
    })
    issue.updated_at = new Date().toISOString()
    return Promise.resolve(issue)
  },
}
