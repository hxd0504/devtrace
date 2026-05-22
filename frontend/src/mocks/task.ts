import type { Task, TaskCreate, TaskUpdate, TaskStatusChangeRequest, TaskDraftRequest, TaskDraftResponse, ExecutorRecommend } from '@/types/task'

const mockTasks: Task[] = [
  {
    id: 1, issue_id: 1, title: '检查路由配置', description: '检查 Vue Router 的路由表配置', status: 'todo',
    owner_name: 'admin', executor_name: 'Claude Code 窗口A', executor_type: 'ai_window', executor_note: null,
    related_files: [], evidence_source: null, evidence_summary: null, acceptance_criteria: null, risk_level: 'low',
    activity_log: [], version: 1,
    created_at: '2026-05-21T11:00:00Z', updated_at: '2026-05-21T11:00:00Z',
  },
]

const mockExecutors: ExecutorRecommend[] = [
  { name: 'Claude Code 窗口A', type: 'ai_window', score: 0.95 },
  { name: 'MiMo', type: 'ai_window', score: 0.88 },
  { name: 'admin', type: 'human', score: 0.70 },
]

export const mockTaskApi = {
  list(_workspaceId: number, _issueId: number): Promise<Task[]> {
    return Promise.resolve(mockTasks)
  },
  create(_workspaceId: number, _issueId: number, data: TaskCreate): Promise<Task> {
    const item: Task = {
      id: mockTasks.length + 1, issue_id: _issueId, title: data.title, description: data.description || null,
      status: 'todo', owner_name: data.owner_name || null, executor_name: data.executor_name || null,
      executor_type: data.executor_type || null, executor_note: data.executor_note || null,
      related_files: data.related_files || [], evidence_source: data.evidence_source || null,
      evidence_summary: data.evidence_summary || null, acceptance_criteria: data.acceptance_criteria || null,
      risk_level: data.risk_level || null,
      activity_log: [], version: 1, created_at: new Date().toISOString(), updated_at: new Date().toISOString(),
    }
    mockTasks.push(item)
    return Promise.resolve(item)
  },
  update(_workspaceId: number, _issueId: number, taskId: number, data: TaskUpdate): Promise<Task> {
    const task = mockTasks.find((x) => x.id === taskId)
    if (!task) return Promise.reject(new Error('Not found'))
    if (task.version !== data.version) return Promise.reject({ response: { status: 409, data: { detail: '版本冲突，请刷新后重试' } } })
    Object.assign(task, { ...data, version: task.version + 1, updated_at: new Date().toISOString() })
    return Promise.resolve(task)
  },
  changeStatus(_workspaceId: number, _issueId: number, taskId: number, data: TaskStatusChangeRequest): Promise<Task> {
    const task = mockTasks.find((x) => x.id === taskId)
    if (!task) return Promise.reject(new Error('Not found'))
    task.status = data.status
    task.version += 1
    task.updated_at = new Date().toISOString()
    task.activity_log.push({
      timestamp: new Date().toISOString(),
      user_id: 1,
      username: 'admin',
      action: 'status_change',
      details: data.details,
    })
    return Promise.resolve(task)
  },
  addNote(_workspaceId: number, _issueId: number, taskId: number, details: string): Promise<Task> {
    const task = mockTasks.find((x) => x.id === taskId)
    if (!task) return Promise.reject(new Error('Not found'))
    task.activity_log.push({
      timestamp: new Date().toISOString(),
      user_id: 1,
      username: 'admin',
      action: 'note',
      details,
    })
    task.updated_at = new Date().toISOString()
    return Promise.resolve(task)
  },
  // V1.1 AI 智能创建
  generateDraft(_data: TaskDraftRequest): Promise<TaskDraftResponse> {
    return Promise.resolve({
      title: '修复 Docker 镜像拉取超时问题',
      description: '分析并解决 Docker 镜像拉取超时的问题，可能与网络代理配置有关',
      executor_type: 'ai_window',
      executor_name: 'Claude Code 窗口A',
      owner_name: 'admin',
      evidence_summary: 'docker pull 命令执行超时，网络连接异常',
      acceptance_criteria: '1. 确认镜像源配置正确\n2. 测试镜像拉取成功\n3. 记录解决方案',
      risk_level: 'medium',
      tags: ['Docker', '网络', '环境配置'],
    })
  },
  getExecutors(_workspaceId: number): Promise<ExecutorRecommend[]> {
    return Promise.resolve(mockExecutors)
  },
}
